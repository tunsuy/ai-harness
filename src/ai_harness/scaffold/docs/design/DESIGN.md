---
# 项目填写：Stitch 兼容 YAML tokens（colors / typography / spacing / rounded / shadows / components）
# 例见 VoltAgent/awesome-design-md 与 Google DESIGN.md 规范。
# 本文件是本仓视觉 SSOT；参照库只影响当轮原型，晋升才改这里。
#
# 可选 lint: 块 —— Layer-1 设计门禁（scripts/design-lint.js）配置：
#   色值/圆角/间距/字号/字重表自动解析自上方各块，无需重复维护；这里只填补充项：
# lint:
#   targets: ["apps/<web>/src"]              # make design-lint 缺省扫描范围
#   heights: [24, 32, 40]                    # 控件高度档位（warning 级；不配则跳过）
#   spacing-extra: [28, 48]                  # spacing 块之外的布局级间距（页面边距/区块 gap）
#   font-sizes-extra: [28, 32]               # typography 角色之外的字号阶梯（metric/display 等）
#   baseline:                                # 已知历史漂移（SSOT 已改、代码禁改期）；折回后必须删条目
#     - "相对路径 | 匹配子串 | 说明（何时折回）"
---

# {{PROJECT_NAME}} — DESIGN.md

> Google Stitch–compatible design system for AI agents and humans.  
> 页模板另文（如 `console-ui.md`）。Tokens here are normative.

## How agents should use this file

1. Read **before** generating any UI / CSS / Tailwind.
2. Use **only** tokens defined in the YAML front matter.
3. Prefer semantic CSS variables mapped 1:1 from these tokens.
4. Follow page skeletons in the project's layout doc; do not invent ad-hoc full-page layouts.
5. Design rounds: pick teachers from [`references/`](./references/README.md); **learn patterns, never copy hex/fonts/logo**.

## Visual theme & atmosphere

（一句话气质 + 对标谁 / 明确不学什么）

## Brand

（mark / 全称 / 简称）

## Colors / Typography / Layout / Elevation / Shapes

（填 token 规则；禁紫渐变、多强调色、mesh 弥散等写进 Don't）

治理模式（TokenStore 实践固化，按需取用）：

- **色板纪律**：① 中性单族（禁混 gray/zinc/neutral 多灰族）；② 单主色 + hover/浅阶变体（第二品牌色仅限营销门面）；③ 语义色 base+soft 成对，**出现消费者才补变体，禁止投机 token**；④ 对比度实测注记（记录不改动——品类通行值不因差半档 AA 就擅自改）；⑤ dark mode 是否目标要显式声明。
- **用色决策表**：场景级规则（图标 / 数据条 / 状态语义 / 文字层级该用什么色）在此查询，不即兴。
- **组件规格矩阵**：每类控件（按钮 / 输入框 / 表格 / 弹窗 / 徽章）给全变体 × 全状态（default/hover/active/focus/disabled）的值，不留「临场拍」空格；配层级纪律（如：每视觉带 1 个 primary、同行 primary 在前、行内按钮统一 sm 档）。
- **表格列对齐成对声明**：表头与单元格的对齐必须成对写（文本左 / 数值右+tnum / 操作列右），改一处必查另一处。

## 质量锚（页面组装质量线）

> Token / 组件是「材料合格」，质量锚是「组装合格」。**原型送人闸前逐条自评，Critic 与 Accept 按此复核**；任何一条不过 = 还没到人闸。
>
> **观感先于核对**：结构判据拦不住「丑」——间距发闷、合成粗体、层级倒挂这类问题锚写不全。所以自查 / Critic 都是**两段式、顺序不可换**：先以「第一次打开页面的用户」身份看三档截图（1440/1024/375）记录所有不适感，然后才逐条对锚。判据回答「过 / 不过 + 定位到哪一段」，观感回答「哪里不舒服 + 为什么」，都不写「感觉还行」。

通用默认锚（项目按产品形态增删改，值以本仓为准）：

1. **一页一语法**：对齐与分栏语法全页一致，不中途切换（混语法是「拼凑感 / 模板腔」最大来源）。
2. **节奏量级统一**：同类 section 纵向间距同一量级，不逐段漂移；背景交替有规律。
3. **产品工件当锚**：需要视觉锚点时用产品自身界面 mockup，不用抽象插画 / 图标堆；mockup 数字标「演示数据」。
4. **字号阶梯不越级**：相邻级对比一次拉开（≥1.6×）；同页同级标题只有一个尺寸。
5. **密度一致**：卡片内边距、栅格 gap、行高全页同量级；项目写明密度下限（区块 gap / 页面边距最小值）。
6. **断点完整**：1440 / 1024 / 375 三档肉眼过——无横向滚动、无孤儿元素。
7. **CJK 已知坑**（产品面向中文时必备防复发清单）：字体栈显式 CJK 回退；中文文本字重 ≤500（600+ 触发合成粗体发闷，600 仅限拉丁标题）；全局 antialiased；中文正文行高 ≥1.5；表头层级用弱化标签流（无底色 + muted 灰 + 400 + 强分隔线）还是组件库流（底色 + 主文字色 + 加粗）——**选定流派写死在这里**，不逐页摇摆。
8. **双语韧性**（产品双语时）：任何「为中文优化」的值晋升前必须过英文校验（字体栈 Latin-first、行高不超英文舒适区、字重策略不拉平拉丁层级）；控件禁定宽截断（中英互译长度差可达 ±30%）；数字用 tabular-nums，日期/千分位 locale 化。

## Do's and Don'ts

### Don't（常见引擎级红线，可删改）

- Don't invent hex outside this file.
- Don't ship purple/lavender/magenta gradient defaults or multi-accent KPI walls.
- Don't copy marketing mesh / cream hero as the product default unless Brief 明确要营销页。

## References

上游灵感：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)；本地取法：[references/README.md](./references/README.md)。  
本文件是 **本仓合成**，不是品牌官方规范拷贝。
