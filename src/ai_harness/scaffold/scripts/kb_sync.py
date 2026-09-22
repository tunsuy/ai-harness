#!/usr/bin/env python3
"""知识库 SSOT：metadata_only 约定 + 域表生成 + context-pack。

子命令: check | check-ship | gen | pack
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
ROADMAP = ROOT / "docs/roadmap.md"
HANDOFF = ROOT / "docs/harness/handoff.md"
BEGIN = "<!-- BEGIN_DOMAINS_TABLE -->"
END = "<!-- END_DOMAINS_TABLE -->"
# 提议中 ADR / 未 approved Brief 前禁止出现在这些路径的 diff 里（相对 main）
CODEISH_PREFIXES = (
    "services/",
    "pkg/",
    "apps/",
    "packages/",
    "api/",
    "src/",
    "deploy/migrations/",
)
TASK_ID_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
# 产品流水线：这些 task 默认不要求 Brief（仍可用 require_brief_approved 显式打开）
BRIEF_EXEMPT_TASKS = frozenset(
    {
        "define-feature",
        "accept-feature",
        "maintain-knowledge",
        "harness-feedback",
        "resume",
        "troubleshoot",
        "l1-micro",
    }
)
BRIEF_STATUSES = frozenset({"draft", "approved", "superseded"})
ACCEPT_STATUSES = frozenset({"in_progress", "PASS", "FAIL"})


def _parse_mini_yaml(text: str) -> dict:
    """零依赖标准库 YAML fallback（支持 domains/tasks 结构的子集）。"""

    def _strip_comment(line: str) -> str:
        in_quote = None
        out = []
        for ch in line:
            if ch in ('"', "'"):
                if in_quote == ch:
                    in_quote = None
                elif in_quote is None:
                    in_quote = ch
            elif ch == "#" and in_quote is None:
                break
            out.append(ch)
        return "".join(out).rstrip()

    def _parse_val(raw: str):
        val = raw.strip()
        if not val:
            return None
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if not inner:
                return []
            res = []
            cur: list[str] = []
            in_q = None
            for ch in inner:
                if ch in ('"', "'"):
                    if in_q == ch:
                        in_q = None
                    elif in_q is None:
                        in_q = ch
                    cur.append(ch)
                elif ch == "," and in_q is None:
                    res.append(_parse_val("".join(cur).strip()))
                    cur = []
                else:
                    cur.append(ch)
            if cur:
                res.append(_parse_val("".join(cur).strip()))
            return res
        if (val.startswith('"') and val.endswith('"')) or (
            val.startswith("'") and val.endswith("'")
        ):
            return val[1:-1]
        if val.lower() == "true":
            return True
        if val.lower() == "false":
            return False
        if val.isdigit():
            return int(val)
        return val

    lines: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        cleaned = _strip_comment(raw_line)
        if cleaned.strip():
            indent = len(cleaned) - len(cleaned.lstrip())
            lines.append((indent, cleaned.strip()))

    def parse_block(idx: int, min_indent: int):
        if idx >= len(lines):
            return {}, idx

        indent, first_line = lines[idx]
        if first_line.startswith("- "):
            items = []
            while idx < len(lines):
                cur_indent, cur_line = lines[idx]
                if cur_indent < indent:
                    break
                if cur_indent == indent and cur_line.startswith("- "):
                    val_str = cur_line[2:].strip()
                    if not val_str:
                        sub_obj, idx = parse_block(idx + 1, indent + 1)
                        items.append(sub_obj)
                    else:
                        items.append(_parse_val(val_str))
                        idx += 1
                else:
                    break
            return items, idx

        obj: dict = {}
        while idx < len(lines):
            cur_indent, cur_line = lines[idx]
            if cur_indent < indent:
                break
            if cur_indent == indent:
                if ":" not in cur_line:
                    idx += 1
                    continue
                colon_pos = cur_line.index(":")
                key = cur_line[:colon_pos].strip()
                val_part = cur_line[colon_pos + 1 :].strip()
                if val_part:
                    obj[key] = _parse_val(val_part)
                    idx += 1
                else:
                    if idx + 1 < len(lines) and lines[idx + 1][0] > cur_indent:
                        sub_obj, idx = parse_block(idx + 1, lines[idx + 1][0])
                        obj[key] = sub_obj
                    else:
                        obj[key] = None
                        idx += 1
            else:
                break
        return obj, idx

    res, _ = parse_block(0, 0)
    return res if isinstance(res, dict) else {}


def load_yaml(path: Path) -> dict:
    raw_text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(raw_text)
    else:
        data = _parse_mini_yaml(raw_text)
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
    """metadata_only：summary / writer / exemplar / extra_files 存在性 + 域表同步。

    路径级归属（文件名=域名等）由项目扩展本函数或参考 examples/。
    """
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
        for adr in t.get("require_adr_accepted") or []:
            if not isinstance(adr, str) or not adr.strip():
                errs.append(f"task {tid}: require_adr_accepted 项非法")
                continue
            if not (ROOT / adr).is_file():
                errs.append(f"task {tid}: require_adr_accepted 不存在: {adr}")
                continue
            st = adr_status(adr)
            if st is None:
                errs.append(f"task {tid}: {adr} 缺少「状态：」行")
            elif st not in ("提议中", "已接受"):
                errs.append(
                    f"task {tid}: {adr} 状态无法识别: {st!r}（须 提议中|已接受）"
                )
        for brief in t.get("require_brief_approved") or []:
            if not isinstance(brief, str) or not brief.strip():
                errs.append(f"task {tid}: require_brief_approved 项非法")
                continue
            if not (ROOT / brief).is_file():
                errs.append(f"task {tid}: require_brief_approved 不存在: {brief}")
                continue
            st = brief_status(brief)
            if st is None:
                errs.append(
                    f"task {tid}: {brief} 缺少状态行（> 状态：`draft`|`approved`）"
                )
            elif st not in BRIEF_STATUSES:
                errs.append(f"task {tid}: {brief} 状态无法识别: {st!r}")
        if t.get("brief_exempt") not in (None, True, False):
            errs.append(f"task {tid}: brief_exempt 须为 bool")
    return errs


def adr_status(rel_path: str) -> str | None:
    """返回 ADR 状态关键词：提议中 / 已接受；无状态行则 None。"""
    text = (ROOT / rel_path).read_text(encoding="utf-8")
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- 状态：") or s.startswith("- 状态:"):
            if "提议中" in s:
                return "提议中"
            if "已接受" in s:
                return "已接受"
            return s.split("：", 1)[-1].split(":", 1)[-1].strip()
    return None


def _status_from_backticks(line: str) -> str | None:
    s = line.strip()
    if "状态" not in s:
        return None
    m = re.search(r"状态\s*[：:]\s*`([^`]+)`", s)
    if m:
        return m.group(1).strip()
    m = re.search(r"状态\s*[：:]\s*(\S+)", s)
    if m:
        return m.group(1).strip().strip("*").strip()
    return None


def brief_status(rel_path: str) -> str | None:
    text = (ROOT / rel_path).read_text(encoding="utf-8")
    for line in text.splitlines()[:40]:
        st = _status_from_backticks(line)
        if st:
            return st
    return None


def accept_status(rel_path: str) -> str | None:
    text = (ROOT / rel_path).read_text(encoding="utf-8")
    for line in text.splitlines()[:40]:
        st = _status_from_backticks(line)
        if st in ACCEPT_STATUSES:
            return st
        if st and st.upper() in ("PASS", "FAIL"):
            return st.upper()
    return None


def feature_brief_path(feature_id: str) -> str:
    return f"docs/features/{feature_id}/brief.md"


def feature_accept_path(feature_id: str) -> str:
    return f"docs/features/{feature_id}/accept.md"


def parse_handoff_meta() -> tuple[str | None, str]:
    meta = parse_handoff_fields()
    return meta.get("status"), meta.get("task") or ""


def parse_handoff_fields() -> dict[str, str | None]:
    out: dict[str, str | None] = {
        "status": None,
        "task": "",
        "feature": "",
        "phase": "",
    }
    if not HANDOFF.is_file():
        return out
    for line in HANDOFF.read_text(encoding="utf-8").splitlines():
        for key in ("status", "task", "feature", "phase"):
            if line.startswith(f"{key}:"):
                raw = line.split(":", 1)[1].strip().strip('"')
                raw = raw.split("#", 1)[0].strip().strip('"')
                if key == "status":
                    out[key] = raw.split()[0] if raw else None
                else:
                    out[key] = raw
    return out


def task_brief_exempt(tid: str, t: dict) -> bool:
    if t.get("brief_exempt") is True:
        return True
    return tid in BRIEF_EXEMPT_TASKS


def roadmap_p0_task_ids() -> list[str]:
    """从 roadmap P0 表 task_id 列提取 id（若项目有 roadmap.md）。"""
    if not ROADMAP.is_file():
        return []
    text = ROADMAP.read_text(encoding="utf-8")
    m = re.search(r"^## P0\b.*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return []
    ids: list[str] = []
    seen: set[str] = set()
    for line in m.group(1).splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*-+", line):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 2:
            continue
        if cols[0] in ("顺序",) or cols[1] == "task_id":
            continue
        cell = cols[1]
        for raw in re.findall(r"`([^`]+)`", cell):
            tid = raw.strip()
            if tid.startswith("DOMAIN=") or tid in ("—", "-") or "进" in tid:
                continue
            if not TASK_ID_RE.match(tid):
                continue
            if tid not in seen:
                seen.add(tid)
                ids.append(tid)
    return ids


def check_roadmap_tasks(task_ids: set[str]) -> list[str]:
    """opt-in：仅当 docs/roadmap.md 存在时校验 P0 task_id ⊆ tasks.yaml。"""
    if not ROADMAP.is_file():
        return []
    errs: list[str] = []
    text = ROADMAP.read_text(encoding="utf-8")
    m = re.search(r"^## P0\b.*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    p0 = roadmap_p0_task_ids()
    if not p0:
        # P0 全部交付是合法终态：占位行须含「已全部交付」标记（明细见 Shipped）
        if not (m and "已全部交付" in m.group(1)):
            errs.append(
                "roadmap P0 表未解析到任何 task_id"
                "（须 `add-…` 反引号；全交付时用「已全部交付」占位行）"
            )
    for tid in p0:
        if tid not in task_ids:
            errs.append(f"roadmap P0 task_id `{tid}` 不在 tasks.yaml")
    return errs


def check_handoff_task(task_ids: set[str]) -> list[str]:
    errs: list[str] = []
    status, task = parse_handoff_meta()
    if status is None:
        return ["docs/harness/handoff.md 不存在"]
    if status not in ("idle", "active", "blocked"):
        errs.append(f"handoff status 非法: {status!r}")
    if status in ("active", "blocked"):
        if not task:
            errs.append(f"handoff status={status} 时 task 不能为空")
        elif task not in task_ids:
            errs.append(f"handoff.task `{task}` 不在 tasks.yaml")
    elif task and task not in task_ids:
        errs.append(f"handoff.task `{task}` 不在 tasks.yaml")
    return errs


def git_changed_vs_main() -> list[str]:
    import subprocess

    paths: set[str] = set()
    for base in ("origin/main", "main"):
        r = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if r.returncode == 0:
            paths.update(p for p in r.stdout.splitlines() if p.strip())
            break
    r2 = subprocess.run(
        ["git", "status", "--porcelain", "-u"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if r2.returncode == 0:
        for line in r2.stdout.splitlines():
            if len(line) < 4:
                continue
            rest = line[3:].strip()
            if " -> " in rest:
                rest = rest.split(" -> ", 1)[1]
            paths.add(rest.strip('"'))
    return sorted(paths)


def is_codeish(path: str) -> bool:
    return any(path.startswith(p) for p in CODEISH_PREFIXES)


def check_adr_accept_before_code(tasks: dict) -> list[str]:
    """active/blocked 且 task 声明 require_adr_accepted：任一仍提议中时，禁止 codeish diff。"""
    status, task = parse_handoff_meta()
    if status not in ("active", "blocked") or not task:
        return []
    t = tasks.get(task) or {}
    adrs = t.get("require_adr_accepted") or []
    if not adrs:
        return []
    pending = [a for a in adrs if adr_status(a) == "提议中"]
    if not pending:
        return []
    dirty = [p for p in git_changed_vs_main() if is_codeish(p)]
    if not dirty:
        return []
    return [
        f"task `{task}` 依赖 ADR 仍为提议中（{', '.join(pending)}），"
        f"但出现代码路径变更（先 Accept 再改业务代码）："
        + ", ".join(dirty[:12])
        + ("…" if len(dirty) > 12 else "")
    ]


def _pending_briefs(t: dict, feature: str) -> list[str]:
    pending: list[str] = []
    for brief in t.get("require_brief_approved") or []:
        if brief_status(brief) != "approved":
            pending.append(brief)
    if feature:
        bp = feature_brief_path(feature)
        if not (ROOT / bp).is_file():
            pending.append(f"{bp}（缺失）")
        elif brief_status(bp) != "approved":
            pending.append(bp)
    return pending


def check_brief_before_code(tasks: dict) -> list[str]:
    """未 approved Brief 禁止抢跑 codeish（产品流水线门禁）。

    触发条件（active|blocked + codeish dirty）任一：
    - task.require_brief_approved 含未 approved
    - handoff.feature 非空且对应 brief 未 approved
    - handoff.phase 为 build|design，且 task 未 brief_exempt → 必须有 feature + approved
    """
    meta = parse_handoff_fields()
    status, task = meta.get("status"), meta.get("task") or ""
    feature = (meta.get("feature") or "").strip()
    phase = (meta.get("phase") or "").strip()
    if status not in ("active", "blocked") or not task:
        return []
    t = tasks.get(task) or {}
    dirty = [p for p in git_changed_vs_main() if is_codeish(p)]
    if not dirty:
        return []

    errs: list[str] = []
    sample = ", ".join(dirty[:12]) + ("…" if len(dirty) > 12 else "")

    explicit = [
        b
        for b in (t.get("require_brief_approved") or [])
        if brief_status(b) != "approved"
    ]
    if explicit:
        errs.append(
            f"task `{task}` 依赖 Brief 未 approved（{', '.join(explicit)}），"
            f"但出现代码路径变更（先 define-feature 人闸再改代码）：{sample}"
        )

    if task_brief_exempt(task, t) and not explicit:
        return errs

    if phase in ("build", "design"):
        if not feature:
            errs.append(
                f"handoff.phase={phase} 且 task `{task}` 非 brief_exempt，"
                f"但 feature 为空（须 docs/features/<id> + Brief approved 才能改代码）：{sample}"
            )
        else:
            pending = _pending_briefs({}, feature)
            if pending:
                errs.append(
                    f"handoff.phase={phase} feature=`{feature}` Brief 未就绪"
                    f"（{', '.join(pending)}），禁止代码路径变更：{sample}"
                )
    elif feature:
        pending = _pending_briefs({}, feature)
        if pending:
            errs.append(
                f"handoff.feature=`{feature}` Brief 未 approved（{', '.join(pending)}），"
                f"禁止代码路径变更：{sample}"
            )

    return errs


def check_accept_pass(tasks: dict) -> list[str]:
    """合入准出：handoff.feature 已挂时 accept.md 须 PASS。

    仅由 check-ship / pr-merge 调用；日常 check 不跑（Build 中途尚无 Accept）。
    """
    meta = parse_handoff_fields()
    feature = (meta.get("feature") or "").strip()
    task = meta.get("task") or ""
    t = tasks.get(task) or {} if task else {}

    need = bool(t.get("require_accept_pass"))
    if feature and task and not task_brief_exempt(task, t):
        need = True
    if feature and (meta.get("phase") or "") == "accept":
        need = True
    if not need:
        return []
    if not feature:
        return [
            "task 声明 require_accept_pass 但 handoff.feature 为空"
            "（须指向 docs/features/<id>）"
        ]

    ap = feature_accept_path(feature)
    if not (ROOT / ap).is_file():
        return [
            f"feature=`{feature}` 须产品验收但缺少 {ap}"
            "（先 accept-feature → PASS 再合入）"
        ]
    st = accept_status(ap)
    if st != "PASS":
        return [
            f"feature=`{feature}` accept 状态为 {st!r}（须 PASS）才能合入："
            f"make context-pack TASK=accept-feature"
        ]
    return []


def resolve_domain_files(name: str, d: dict, _data: dict) -> list[str]:
    files: list[str] = []
    for f in [d.get("exemplar") or "", *(d.get("extra_files") or [])]:
        if f and f not in files:
            files.append(f)
    return files


def cmd_check() -> int:
    dom = load_yaml(DOMAINS)
    tsk = load_yaml(TASKS)
    tasks = tsk.get("tasks") or {}
    task_ids = set(tasks)
    errs = (
        check_domains(dom)
        + check_tasks(tsk, set((dom.get("domains") or {})))
        + check_roadmap_tasks(task_ids)
        + check_handoff_task(task_ids)
        + check_adr_accept_before_code(tasks)
        + check_brief_before_code(tasks)
    )
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
    if ROADMAP.is_file():
        print("  [PASS] roadmap P0 task_id ⊆ tasks.yaml（若有）")
    print("  [PASS] handoff.task 合法")
    print("  [PASS] 提议中 ADR 未抢跑代码路径")
    print("  [PASS] Brief 未 approved 未抢跑代码路径")
    print("KB sync: OK")
    return 0


def cmd_check_ship() -> int:
    """合入前产品准出（Brief 闸 + Accept PASS）。供 pr-merge 调用。"""
    ec = cmd_check()
    if ec != 0:
        return ec
    # 先跑完整 check（合入闸 ⊇ 日常门禁）
    tsk = load_yaml(TASKS)
    tasks = tsk.get("tasks") or {}
    errs = check_accept_pass(tasks)
    if errs:
        print("==> product ship gate FAIL")
        for e in errs:
            print(f"  [FAIL] {e}")
        return 1
    print("  [PASS] feature Accept 准出（check-ship）")
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
    pending = [
        a for a in (t.get("require_adr_accepted") or []) if adr_status(a) == "提议中"
    ]
    if pending:
        print("WARN: 下列 ADR 仍为提议中 — 先 Accept 再改业务代码：")
        for a in pending:
            print(f"  - {a}")
    brief_pending = [
        b
        for b in (t.get("require_brief_approved") or [])
        if brief_status(b) != "approved"
    ]
    meta = parse_handoff_fields()
    feat = (meta.get("feature") or "").strip()
    if feat:
        bp = feature_brief_path(feat)
        if not (ROOT / bp).is_file() or brief_status(bp) != "approved":
            brief_pending.append(bp)
    if brief_pending:
        print("WARN: 下列 Feature Brief 未 approved — 先 define-feature 人闸再改代码：")
        for b in brief_pending:
            print(f"  - {b}")
    if task_brief_exempt(task, t):
        print("NOTE: 本 task brief_exempt（微改/元任务）；新功能请走 define-feature")
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
    sub.add_parser("check-ship", help="合入前：check + Accept PASS")
    sub.add_parser("gen")
    p = sub.add_parser("pack")
    p.add_argument("task")
    p.add_argument("--domain", default=None)
    args = ap.parse_args()
    if args.cmd == "check":
        return cmd_check()
    if args.cmd == "check-ship":
        return cmd_check_ship()
    if args.cmd == "gen":
        return cmd_gen()
    if args.cmd == "pack":
        return cmd_pack(args.task, args.domain)
    return 2


if __name__ == "__main__":
    sys.exit(main())
