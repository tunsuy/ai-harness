#!/usr/bin/env python3
"""知识库 SSOT：metadata_only 约定 + 域表生成 + context-pack。

子命令: check | gen | pack
项目若需路径级归属，在本文件扩展 check_domains()，参见 ai-harness/examples/。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ROOT / "docs/harness/domains.yaml"
TASKS = ROOT / "docs/harness/tasks.yaml"
ARCH = ROOT / "docs/architecture.md"
BEGIN = "<!-- BEGIN_DOMAINS_TABLE -->"
END = "<!-- END_DOMAINS_TABLE -->"


def load_yaml(path: Path) -> dict:
    if yaml is None:
        sys.exit("FAIL: 需要 PyYAML（pip3 install -r scripts/requirements-kb.txt）")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        sys.exit(f"FAIL: {path} 根须为 mapping")
    return data


def gen_table(domains: dict) -> str:
    lines = [
        "| 域 | 定义与不变量 | 写所有者 | 表 / 缓存 | 样板 |",
        "|----|--------------|----------|-----------|------|",
    ]
    for name, d in domains.items():
        tables = ", ".join(f"`{t}`" for t in d.get("tables") or []) or "—"
        caches = ", ".join(f"`{c}`" for c in d.get("caches") or [])
        tc = tables if not caches else (f"{tables}；{caches}" if tables != "—" else caches)
        ex = d.get("exemplar") or "—"
        summary = (d.get("summary") or "").replace("|", "\\|")
        writer = d.get("writer") or "—"
        lines.append(f"| **{name}** | {summary} | {writer} | {tc} | `{ex}` |")
    return "\n".join(lines) + "\n"


def write_arch_table(table: str) -> None:
    text = ARCH.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        sys.exit(f"FAIL: {ARCH} 缺少 {BEGIN} / {END} 标记")
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    new_text, n = pattern.subn(f"{BEGIN}\n{table}{END}", text, count=1)
    if n != 1:
        sys.exit("FAIL: 无法替换 architecture 域表标记区")
    ARCH.write_text(new_text, encoding="utf-8")


def expected_arch_section(domains: dict) -> str:
    return f"{BEGIN}\n{gen_table(domains)}{END}"


def check_arch_in_sync(domains: dict) -> list[str]:
    if not ARCH.is_file():
        return [f"缺少 {ARCH}"]
    text = ARCH.read_text(encoding="utf-8")
    m = re.search(re.escape(BEGIN) + r"(.*?)" + re.escape(END), text, re.S)
    if not m:
        return [f"{ARCH.name} 缺少域表标记 {BEGIN} .. {END}"]

    def norm(s: str) -> str:
        return "\n".join(line.rstrip() for line in s.strip().splitlines())

    if norm(m.group(0)) != norm(expected_arch_section(domains)):
        return ["architecture.md 域表与 domains.yaml 不同步 —— 请运行: make kb-gen"]
    return []


def check_domains(data: dict) -> list[str]:
    errs: list[str] = []
    domains: dict = data.get("domains") or {}
    if not domains:
        return ["domains.yaml 无 domains"]

    for name, d in domains.items():
        if not d.get("summary"):
            errs.append(f"域 {name}: 缺少 summary")
        if not d.get("writer"):
            errs.append(f"域 {name}: 缺少 writer")
        exf = d.get("exemplar")
        if not exf:
            errs.append(f"域 {name}: 缺少 exemplar（冷启动样板）")
        elif not (ROOT / exf).is_file():
            errs.append(f"域 {name}: exemplar 不存在: {exf}")
        for f in d.get("extra_files") or []:
            if not (ROOT / f).is_file():
                errs.append(f"域 {name}: extra_files 不存在: {f}")

    errs.extend(check_arch_in_sync(domains))
    return errs


def check_tasks(data: dict, domain_names: set[str]) -> list[str]:
    errs: list[str] = []
    for tid, t in (data.get("tasks") or {}).items():
        pb = t.get("playbook") or ""
        if pb and not (ROOT / pb).is_file():
            errs.append(f"task {tid}: playbook 不存在: {pb}")
        for f in t.get("must_read") or []:
            if not (ROOT / f).is_file():
                errs.append(f"task {tid}: must_read 不存在: {f}")
        d = t.get("domain")
        if d and d not in domain_names:
            errs.append(f"task {tid}: domain {d} 不在 domains.yaml")
    return errs


def resolve_domain_files(name: str, d: dict, _data: dict) -> list[str]:
    files: list[str] = []
    for f in [d.get("exemplar") or "", *(d.get("extra_files") or [])]:
        if f and f not in files:
            files.append(f)
    return files


def cmd_check() -> int:
    dom = load_yaml(DOMAINS)
    tsk = load_yaml(TASKS)
    errs = check_domains(dom) + check_tasks(tsk, set((dom.get("domains") or {})))
    if errs:
        print("==> KB sync FAIL")
        for e in errs:
            print(f"  [FAIL] {e}")
        print(f"KB sync: 0 通过, {len(errs)} 失败")
        return 1
    print("==> KB sync（metadata_only）")
    print("  [PASS] 域元数据 + exemplar")
    print("  [PASS] architecture 域表与 domains.yaml 同步")
    print("  [PASS] tasks.yaml 路径有效")
    print("KB sync: 3 通过, 0 失败")
    return 0


def cmd_gen() -> int:
    dom = load_yaml(DOMAINS)
    write_arch_table(gen_table(dom.get("domains") or {}))
    print(f"已根据 {DOMAINS.relative_to(ROOT)} 重写 {ARCH.relative_to(ROOT)} 域表")
    return 0


def cmd_pack(task: str, domain: str | None) -> int:
    tsk = load_yaml(TASKS)
    dom = load_yaml(DOMAINS)
    tasks = tsk.get("tasks") or {}
    if task not in tasks:
        print(f"未知 task: {task}", file=sys.stderr)
        print("可选: " + ", ".join(sorted(tasks)), file=sys.stderr)
        return 2
    t = tasks[task]
    if t.get("require_domain") and not domain:
        print(f"task {task} 需要 --domain", file=sys.stderr)
        print("可选域: " + ", ".join(sorted(dom.get("domains") or {})), file=sys.stderr)
        return 2
    domain = domain or t.get("domain")
    files: list[str] = []
    for f in t.get("must_read") or []:
        if f not in files:
            files.append(f)
    if domain:
        d = (dom.get("domains") or {}).get(domain)
        if not d:
            print(f"未知 domain: {domain}", file=sys.stderr)
            return 2
        for f in resolve_domain_files(domain, d, dom):
            if f not in files:
                files.append(f)
    pb = t.get("playbook") or ""
    if pb and pb not in files:
        files.insert(0, pb)

    print("=== COLD START — 只读下列文件后再改代码；禁止先做全库 Glob/Grep ===")
    print(f"task={task}" + (f" domain={domain}" if domain else ""))
    if t.get("summary"):
        print(f"summary: {t['summary']}")
    print("---")
    for i, f in enumerate(files, 1):
        exists = "OK" if (ROOT / f).is_file() else "MISSING"
        print(f"{i:2}. [{exists}] {f}")
    print("---")
    print("改域元数据后: make kb-gen && make check-harness")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Knowledge-base sync (ai-harness)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("gen")
    p = sub.add_parser("pack")
    p.add_argument("task")
    p.add_argument("--domain", default=None)
    args = ap.parse_args()
    if args.cmd == "check":
        return cmd_check()
    if args.cmd == "gen":
        return cmd_gen()
    if args.cmd == "pack":
        return cmd_pack(args.task, args.domain)
    return 2


if __name__ == "__main__":
    sys.exit(main())
