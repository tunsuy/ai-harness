# 中文设计系统 token 对照（Ant Design / Arco Design / TDesign）

> 用途：**token 级的老师**——和 `awesome-design-md`（整页观感参照）互补，这里回答「中文界面的一格字号、一档字重、一个表头到底该是什么值」。三家源码为证，不是二手解读。
> 日期：2026-09-16
> 来源（三家开源仓库，main/default 分支）：
> - Ant Design（阿里）`ant-design/ant-design`
> - Arco Design（字节）`arco-design/arco-design`（原 web-react 仓已 404，现为合并主仓）
> - TDesign（腾讯）`Tencent/tdesign-common`（default 分支 develop）
> 出处：成文于首个消费者 **TokenStore** 的实战（文中「我们 / 本仓」指 TokenStore）。**取法与纪律是引擎默认；具体 token 决策不是**——各项目参照本方法挖值、晋升进自己的 DESIGN.md。

## 取法（与 awesome-design-md 的差异）

1. **只挖 token，不搬组件**：字号 / 行高 / 字重 / 密度 / 灰阶 / 间距——这些是「值」，直接进 DESIGN.md 决策依据；组件实现（React/Vue 结构）一律不学，我们不引入组件库。
2. **三家共识 = 硬标准**；一家独有 = 记下来但非强制（可解释为什么）。两家一致时按多数，但必须核对第三家的反例是否更贴合我们的约束（例：表头字重三家三分，我们选 Arco 500 是因为 Windows 合成粗体问题，不是简单多数）。
3. 拉取用 curl GitHub API + raw.githubusercontent.com（WebFetch 对 github.com 不可用）。

## 对照结果（2026-09-16 源码实查）

### 字体栈

| 家 | 栈 | 证据 |
|---|---|---|
| Ant | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif…` | `components/theme/themes/seed.ts` |
| Arco | `Inter, -apple-system, BlinkMacSystemFont, PingFang SC, Hiragino Sans GB, noto sans, Microsoft YaHei…` | `components/style/theme/default.less` |
| TDesign | `PingFang SC, Microsoft YaHei, Arial Regular`（中文放最前） | `style/web/theme/_font.less` |

- **Ant 的栈里没有中文字体**——中文渲染全靠浏览器兜底，这是 Ant 长期被吐槽的点，别学。
- **Arco 模式 = 我们的现行做法**：拉丁字体在前（拉丁字形取 Inter/系统 UI 的清晰度）+ PingFang SC 等中文回退（中文回退到平台中文字体），浏览器按字形逐个回退，两全。
- TDesign 把 PingFang SC 放第一，拉丁字形也用苹方的拉丁（牺牲拉丁锐度换一致性）——console 数字密度高，**拉丁优先更适合我们**。

### 字号 × 行高（三家 14px 正文殊途同归）

| 家 | 行高策略 | 14px 对应 | 证据 |
|---|---|---|---|
| Ant | 算法 `(size+8)/size`，h1-h5 = 38/30/24/20/16 | 1.5714 ≈ 22px | `theme/themes/default/index.ts` |
| Arco | 全局 1.5715，title 16/20/24 | 1.5715 ≈ 22px | `style/theme/default.less` |
| TDesign | **绝对 px**（14px → 22px），title S/M/L/XL = 14/16/18/20（行高 22/24/26/28） | 22px | `style/web/theme/_font.less` |

**三家共识：14px 正文 → 22px 行高。** TDesign 的绝对 px 写法对 CJK 更可控（倍数行高在奇数字号下产生小数像素），`(size+8)` 算法是速记（12→20、14→22、16→24、20→28、24→32）。

### 表头规格（三家做法对照，我们决策的依据）

| 维度 | Ant | Arco | TDesign |
|---|---|---|---|
| 底色 | 有（黑 4% 叠白 colorFillAlterSolid） | 有（neutral-2 `rgb(242,243,245)`） | **无**（继承白底） |
| 文字色 | **主文字色 88%** | **主文字色 gray-10 `rgb(29,33,41)`** | 40% 黑（比正文弱化） |
| 字重 | 600 | 500 | 400（不加粗） |
| 字号 | 14 = 正文 | 14 = 正文 | 14 = 正文 |

- 三家共同点只有一条：**表头字号 = 正文 14px**（印证我们锚 ⑦「表头 ≥ 正文」）。
- **表头文字色：Ant 和 Arco 都用主文字色，不用次级色**——层级靠底色 + 字重，不靠把字变灰。
- TDesign 反着做（不加粗 + 弱化文字）也成立，说明表头层级存在两个成熟流派；**我们选 Arco 流**（底色 + 500 + 主文字色），理由：① 与锚 ⑦ 现行结构一致，只改文字色一档；② Ant 的 600 在 Windows 微软雅黑上触发合成粗体（锚 ⑦ 明令回避）；③ TDesign 流是「弱化」，和我们「表头要和正文有差异性」的诉求相反。

### 单元格密度（三档 padding，vertical × horizontal）

| 档 | Ant | Arco | TDesign |
|---|---|---|---|
| default | 16×16 | 9×16 | 12×16 |
| middle/small | 12×8 | 7×16 | 8×8（small） |
| large | — | — | 16×32 |

**admin console 的主流默认在 9–16px 垂直之间**；TDesign（腾讯为中后台而生）默认 12×16。我们的 14×16 略偏松，归到 12×16 与 TDesign 同档。

### 中性灰阶（文字层级）

| 层级 | Ant | Arco | TDesign |
|---|---|---|---|
| 主文字 | 黑 88% | `rgb(29,33,41)` | 黑 90% |
| 次文字 | 黑 65% | `rgb(78,89,105)` | 黑 60% |
| 弱/占位 | 黑 45% | `rgb(134,144,156)` | 黑 40% |
| 禁用/边 | 黑 25% | `rgb(201,205,212)` | 黑 26% |

共识：主文字 88–90% 黑（**非纯黑**，留呼吸）；透明度黑或冷灰阶（非暖灰）。

### 间距体系

- Ant：4px 网格（4/8/12/16/20/24/32/48）。
- Arco：4 的倍数（2px 起步，更细的档）。
- TDesign：4px 网格（2/4/6/8/12/16/20/24/28/32/36/40/48/56/64/72）。
- **共识：4px 节奏**，与我们 spacing token 一致，无需改。

## 晋升进 DESIGN.md 的决策（2026-09-16，keys v4 起）

> 案例日志（TokenStore）——演示「参照 → 晋升」机制如何运转，值本身不是引擎默认。注意演进：下方第 3 条（表头 ink 主文字色 + 底色）后来在人闸反馈中被修订为**弱化标签流**（无底色 + ink-muted + 400 + hairline-strong），参照结论也会随实测迭代，以项目 DESIGN.md 现行为准。

1. 字体栈维持 Arco 模式（拉丁优先 + CJK 回退）——已有，证据补强。
2. 行高策略改 **绝对 px + `(size+8)` 算法**：正文 14/22（我们现行 1.6≈22.4px，收敛到 22px）。
3. 表头文字色 ink-secondary → **ink（主文字色）**；底色 + 字重 500 + hairline-strong 维持。
4. 单元格默认密度收敛到 **12×16**（TDesign 中后台同档，v3 的 14×16 略松）。
5. 控件规格整套晋升（细表见 `controls.md`）：高度档位 **24/32/40**、输入框 focus **2px 主色浅阶外圈**、复选/单选 **16px**、弹窗 **480/12/24/16-500**；分歧裁决——按钮字重三家 400 → 我们取 500（中文 400 偏软）、圆角三家 2–6 → 维持我们 8、Arco 无边框输入框弃。

## 纪律

- 同 awesome-design-md：**学值不搬组件**，任何一家的 React/Vue 实现不进我们的库。
- 三家 token 值本身（hex、具体 px）不直接进 DESIGN.md token 体系——进的是**决策和量级**（例「14→22」这个关系，不是 Arco 的灰阶色值）。
- 本文件记录的是 2026-09-16 的源码快照结论；三家演进后需复核的，拉对应源文件 diff。
