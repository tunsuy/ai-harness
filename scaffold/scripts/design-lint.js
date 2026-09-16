#!/usr/bin/env node
/**
 * Design Token Compliance Linter（ai-harness 引擎 · Layer 1 设计门禁）
 *
 * 扫描 CSS/TSX/TS/HTML，检查硬编码值是否命中项目 DESIGN.md token 表：
 *   error（阻断）：表外 hex 色值 / 圆角 / 字号 / 字重
 *   warning（提示）：表外 rgba / 控件高度 / 间距
 *   baseline（已知漂移，不阻断）：DESIGN.md `lint.baseline` 登记的条目——
 *     用于「SSOT 已更新但代码处于禁改期」的过渡，折回后必须删除条目。
 *
 * Token 来源 = 项目 `docs/design/DESIGN.md` YAML front matter（Stitch 兼容），零依赖内置解析：
 *   colors:    块内 hex → 色值表；rgba 三元组 → rgba 白名单
 *   rounded:   px 值 → 圆角档位
 *   spacing:   px 值 → 间距档位
 *   typography.*.fontSize / fontWeight → 字号 / 字重档位（全 front matter 扫描）
 *   shadows:   rgba 三元组 → rgba 白名单
 *   lint:      （可选）门禁配置——
 *     targets: ["apps/web/src", ...]     无命令行参数时的默认扫描范围
 *     heights: [24, 32, 40]              控件高度档位（warning 级；不配则跳过高度检查）
 *     spacing-extra: [28, ...]           spacing 块之外的布局级间距补充
 *     font-sizes-extra: [28, ...]        typography 之外的正文字号阶梯补充
 *     baseline:                          已知历史漂移（Build 折回后必须删除）
 *       - "相对路径 | 匹配子串 | 说明"
 *
 * 结构性 rgba 恒定放行：rgba(255,255,255,*)（内高光）/ rgba(0,0,0,*)（遮罩）。
 * 全圆场景豁免圆角档位：9999px / 50% / rounded-full / avatar / dot / circle 上下文。
 *
 * 用法：node scripts/design-lint.js [targets...]   （缺省读 lint.targets）
 * 退出码：0 = 通过（可含 warning/baseline）；1 = 有 error；2 = 配置/环境错误。
 *
 * 边界：本脚本只管「值命中 token 表」（Layer 1）。组件结构合规（Layer 2 AST）
 * 与质量锚自动核对（Layer 3 Playwright）不在这里做。
 */

const fs = require('fs');
const path = require('path');

// ========== DESIGN.md front matter 迷你解析（零依赖，支持 Stitch 子集） ==========

function findDesignDoc(explicit) {
  const candidates = explicit
    ? [explicit]
    : ['docs/design/DESIGN.md', 'DESIGN.md'];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

function extractFrontMatter(content) {
  const m = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  return m ? m[1] : null;
}

// 取某个顶层块（如 colors:）的原文段落：从 `key:` 行到下一个顶层 key 行为止
function blockSection(fm, key) {
  const lines = fm.split(/\r?\n/);
  const out = [];
  let inside = false;
  for (const line of lines) {
    if (/^[A-Za-z_-]+:/.test(line)) {
      const isTarget = line.startsWith(key + ':');
      if (inside && !isTarget) break;
      inside = isTarget;
      continue;
    }
    if (inside) out.push(line);
  }
  return out.join('\n');
}

function parseFlowList(str) {
  // [a, "b", 3] → ['a','b','3']
  const inner = str.replace(/[\[\]]/g, '');
  return inner.split(',').map(s => s.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
}

function parseTokens(designPath) {
  const content = fs.readFileSync(designPath, 'utf8');
  const fm = extractFrontMatter(content);
  if (!fm) {
    console.error(`❌ ${designPath}: 找不到 YAML front matter（--- 包围的 token 块）`);
    process.exit(2);
  }

  const colorsBlock = blockSection(fm, 'colors');
  const roundedBlock = blockSection(fm, 'rounded');
  const spacingBlock = blockSection(fm, 'spacing');
  const shadowsBlock = blockSection(fm, 'shadows');
  const lintBlock = blockSection(fm, 'lint');

  const colors = [...new Set((colorsBlock.match(/#[0-9a-fA-F]{3,8}\b/g) || []).map(normalizeHex))];
  const rgbaTriples = new Set();
  for (const block of [colorsBlock, shadowsBlock]) {
    for (const m of block.matchAll(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/g)) {
      rgbaTriples.add(`${m[1]},${m[2]},${m[3]}`);
    }
  }
  const radii = [...new Set((roundedBlock.match(/(\d+(?:\.\d+)?)px/g) || []).map(s => parseFloat(s)))];
  const spacing = [...new Set((spacingBlock.match(/(\d+(?:\.\d+)?)px/g) || []).map(s => parseFloat(s)))];
  const fontSizes = [...new Set((fm.match(/fontSize:\s*(\d+(?:\.\d+)?)px/g) || []).map(s => parseFloat(s.replace(/[^0-9.]/g, ''))))];
  const fontWeights = [...new Set((fm.match(/fontWeight:\s*(\d+)/g) || []).map(s => parseInt(s.replace(/\D/g, ''), 10)))];

  // lint: 配置块
  const lint = { targets: [], heights: null, baseline: [] };
  const tM = lintBlock.match(/targets:\s*\[([^\]]*)\]/);
  if (tM) lint.targets = parseFlowList('[' + tM[1] + ']');
  const hM = lintBlock.match(/heights:\s*\[([^\]]*)\]/);
  if (hM) lint.heights = parseFlowList('[' + hM[1] + ']').map(Number).filter(n => !isNaN(n));
  const seM = lintBlock.match(/spacing-extra:\s*\[([^\]]*)\]/);
  if (seM) spacing.push(...parseFlowList('[' + seM[1] + ']').map(Number).filter(n => !isNaN(n)));
  const feM = lintBlock.match(/font-sizes-extra:\s*\[([^\]]*)\]/);
  if (feM) fontSizes.push(...parseFlowList('[' + feM[1] + ']').map(Number).filter(n => !isNaN(n)));
  for (const m of lintBlock.matchAll(/-\s*"([^"]+\|[^"]+)"/g)) {
    const parts = m[1].split('|').map(s => s.trim());
    if (parts.length >= 2) lint.baseline.push({ file: parts[0], needle: parts[1], note: parts[2] || '' });
  }

  return { colors, rgbaTriples, radii, spacing, fontSizes, fontWeights, lint };
}

// ========== 值提取与规范化 ==========

function normalizeHex(hex) {
  let h = hex.toLowerCase();
  if (/^#[0-9a-f]{3}$/.test(h)) h = '#' + h[1] + h[1] + h[2] + h[2] + h[3] + h[3];
  if (/^#[0-9a-f]{8}$/.test(h)) h = h.slice(0, 7);
  return h;
}

function extractColors(content) {
  // \b 收尾：排除 href="#features" 这类锚点误报
  const hexColors = content.match(/#[0-9a-fA-F]{3,8}\b/g) || [];
  const rgbColors = content.match(/rgba?\([^)]+\)/g) || [];
  return { hexColors, rgbColors };
}

function extractNumbers(content, property) {
  const regex = new RegExp(`${property}:\\s*([\\d.]+)(px|rem|em)?`, 'g');
  const matches = [];
  let m;
  while ((m = regex.exec(content)) !== null) {
    matches.push({ value: parseFloat(m[1]), unit: m[2] || 'px' });
  }
  return matches;
}

const FULL_ROUND_KEYWORDS = ['9999px', '50%', 'rounded-full'];
const FULL_ROUND_CONTEXT = ['avatar', 'dot', 'circle'];

// ========== 单文件检查 ==========

function checkFile(filePath, tokens) {
  const content = fs.readFileSync(filePath, 'utf8');
  const errors = [];
  const warnings = [];

  // 1. hex 色值（严格：表外即 error）
  const { hexColors, rgbColors } = extractColors(content);
  const seenHex = new Set();
  for (const color of hexColors) {
    const normalized = normalizeHex(color);
    if (seenHex.has(normalized)) continue;
    seenHex.add(normalized);
    if (!tokens.colors.includes(normalized)) {
      errors.push(`[COLOR] ${filePath}: 硬编码色值 ${color} 不在 DESIGN.md token 表中`);
    }
  }

  // 2. rgba（三元组命中 front matter 派生白名单，或结构性黑/白 → 放行；否则 warning）
  for (const color of rgbColors) {
    const m = color.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
    if (!m) continue;
    const triple = `${m[1]},${m[2]},${m[3]}`;
    const structural = triple === '255,255,255' || triple === '0,0,0';
    if (!structural && !tokens.rgbaTriples.has(triple)) {
      warnings.push(`[COLOR] ${filePath}: rgba 色值 ${color} 三元组不在 DESIGN.md 派生白名单中，请确认`);
    }
  }

  // 3. 控件高度（仅当 lint.heights 配置时；warning 级）
  if (tokens.lint.heights && tokens.lint.heights.length) {
    for (const { value, unit } of extractNumbers(content, 'height')) {
      if (unit === 'px' && value >= 16 && value <= 64 && !tokens.lint.heights.includes(value)) {
        if (!content.includes('avatar') && !content.includes('row-height')) {
          warnings.push(`[HEIGHT] ${filePath}: 高度 ${value}px 不在控件档位表 [${tokens.lint.heights}] 中`);
        }
      }
    }
  }

  // 4. 圆角（error 级；仅匹配 px 值——50%/9999px 全圆写法天然豁免，另有上下文关键词豁免）
  const seenRadius = new Set();
  for (const m of content.matchAll(/border-radius:\s*([\d.]+)px/g)) {
    const value = parseFloat(m[1]);
    if (tokens.radii.includes(value) || seenRadius.has(value)) continue;
    seenRadius.add(value);
    const context = content.substring(Math.max(0, m.index - 60), m.index + 60);
    const isFullRound = FULL_ROUND_KEYWORDS.some(k => context.includes(k)) ||
                        FULL_ROUND_CONTEXT.some(k => context.includes(k));
    if (!isFullRound) {
      errors.push(`[RADIUS] ${filePath}: 圆角 ${value}px 不在档位表 [${tokens.radii}] 中`);
    }
  }

  // 5. 间距（warning 级）
  for (const prop of ['padding', 'margin', 'gap']) {
    for (const { value, unit } of extractNumbers(content, prop)) {
      if (unit === 'px' && value > 0 && !tokens.spacing.includes(value)) {
        warnings.push(`[SPACING] ${filePath}: ${prop} ${value}px 不在间距表中`);
      }
    }
  }

  // 6. 字号（error 级）
  for (const { value, unit } of extractNumbers(content, 'font-size')) {
    if (unit === 'px' && !tokens.fontSizes.includes(value)) {
      errors.push(`[FONT-SIZE] ${filePath}: 字号 ${value}px 不在档位表 [${tokens.fontSizes.sort((a, b) => a - b)}] 中`);
    }
  }

  // 7. 字重（error 级；front matter 未定义字重时跳过）
  if (tokens.fontWeights.length) {
    for (const { value } of extractNumbers(content, 'font-weight')) {
      if (!tokens.fontWeights.includes(value)) {
        errors.push(`[FONT-WEIGHT] ${filePath}: 字重 ${value} 不在档位表 [${tokens.fontWeights.sort((a, b) => a - b)}] 中`);
      }
    }
  }

  return { errors, warnings };
}

// ========== 主流程 ==========

function main() {
  const args = process.argv.slice(2);
  let designPath = null;
  const targets = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--design' && args[i + 1]) { designPath = args[++i]; }
    else targets.push(args[i]);
  }

  designPath = findDesignDoc(designPath);
  if (!designPath) {
    console.log('未找到 docs/design/DESIGN.md，跳过设计门禁（项目尚未建立设计 SSOT）');
    process.exit(0);
  }

  const tokens = parseTokens(designPath);
  if (!tokens.colors.length) {
    // 骨架未填（init 后还没写 token）：门禁优雅跳过，不阻塞工程
    console.log(`${designPath}: colors 块为空（设计 SSOT 尚未填写），跳过设计门禁`);
    process.exit(0);
  }

  const scanTargets = targets.length ? targets : tokens.lint.targets;
  if (!scanTargets.length) {
    console.log('未指定扫描目标且 DESIGN.md lint.targets 为空，跳过。用法：node scripts/design-lint.js <dir|file>...');
    process.exit(0);
  }

  const exts = ['.css', '.tsx', '.ts', '.html'];
  let allErrors = [];
  let allWarnings = [];

  function walk(target) {
    const stat = fs.statSync(target);
    if (stat.isFile()) {
      if (exts.includes(path.extname(target))) {
        const r = checkFile(target, tokens);
        allErrors = allErrors.concat(r.errors);
        allWarnings = allWarnings.concat(r.warnings);
      }
      return;
    }
    for (const entry of fs.readdirSync(target)) {
      if (entry.startsWith('.') || entry === 'node_modules' || entry === 'dist') continue;
      walk(path.join(target, entry));
    }
  }

  for (const t of scanTargets) {
    if (fs.existsSync(t)) walk(t);
    else console.log(`目录 ${t} 不存在，跳过...`);
  }

  // 历史漂移基线：命中 lint.baseline 的 error 降级（Build 折回后须删条目）
  const baseline = [];
  const realErrors = allErrors.filter(err => {
    const hit = tokens.lint.baseline.find(d => err.includes(d.file) && err.includes(d.needle));
    if (hit) {
      baseline.push(`[BASELINE] ${err}  ← 已知漂移：${hit.note}`);
      return false;
    }
    return true;
  });

  if (baseline.length) {
    console.log('\n🕒 KNOWN DRIFT（基线内，折回后须从 DESIGN.md lint.baseline 删除）:');
    baseline.forEach(b => console.log('  ' + b));
  }
  if (allWarnings.length) {
    console.log('\n⚠️  WARNINGS:');
    allWarnings.forEach(w => console.log('  ' + w));
  }

  if (realErrors.length) {
    console.log('\n❌ ERRORS:');
    realErrors.forEach(e => console.log('  ' + e));
    console.log(`\n${realErrors.length} error(s), ${allWarnings.length} warning(s), ${baseline.length} baseline`);
    process.exit(1);
  }
  console.log(`\n✅ Design token check passed (${allWarnings.length} warnings, ${baseline.length} baseline) — tokens from ${designPath}`);
  process.exit(0);
}

main();
