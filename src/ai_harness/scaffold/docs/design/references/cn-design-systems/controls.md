# 控件级 token 对照（Ant Design / Arco Design / TDesign）

> 用途：`README.md` 回答「字/灰阶/间距该是什么值」，本文件回答「**控件本身**的高度档位、padding、圆角、focus 态该是什么值」——按钮多高、输入框 focus 外圈几像素、Modal 内边距多大。三家源码为证，不是二手解读。
> 日期：2026-09-16
> 来源（与 README 同一批仓库快照）：
> - Ant Design（v5，`ant-design/ant-design` master）：`components/theme/themes/seed.ts`（全局 seed）+ 各组件 `style/` 下的 `token.ts` / `index.ts`（v5 组件值多为「seed 派生表达式」，本文同时给出表达式和默认代入值）
> - Arco Design（字节，`arco-design/arco-design` main）：各组件 `style/token.less`（组件值的权威来源）+ `components/style/theme/global.less`（全局变量）
> - TDesign（腾讯，`Tencent/tdesign-common` develop）：`style/web/theme/_size.less` / `_radius.less` / `_light.less`（全局 CSS 变量）+ `style/web/components/<组件>/_var.less`（组件变量）

## 取法

1. 同 README：**只挖 token，不搬组件**。只记事实值 + 出处，评价性的取舍不在本文件做。
2. AntD v5 的值分两层：seed 值（`controlHeight: 32`、`borderRadius: 6`）是显式常量；档位值是**派生公式**（`controlHeightSM = controlHeight × 0.75` 等），表中给出「公式 = 默认值」双写法——公式意味着改 seed 会联动，这在别家是静态查表做不到的。
3. Arco / TDesign 的档位值是**静态常量表**，直接引用即可。TDesign 的 less 变量全部映射到 CSS 变量（`@comp-size-m` → `var(--td-comp-size-m)`），本文统一写解析后的 px 值并标注 CSS 变量名。
4. 圆角/主色各家语义名不同（AntD `borderRadius` / Arco `radius-medium` / TDesign `radius-default`），对照时以 px 值对齐。

---

## 1. 按钮

| 维度 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| 档位数 | 3（small/default/large） | 4（mini/small/default/large） | 3（s/default/l） |
| 高度 | sm 24 / **default 32** / lg 40（`controlHeightSM=×0.75`、`LG=×1.25`） | mini 24 / small 28 / **default 32** / large 36（`@size-mini`…`@size-large`） | s 24 / **default 32**（`--td-comp-size-m`）/ l 40（`--td-comp-size-xl`） |
| 水平 padding | default & lg **15**（`paddingContentHorizontal(16)−lineWidth(1)`）、sm **7**（`8−1`） | mini 11 / small 15 / **default 15** / large 19 | s 8（`--td-comp-paddingLR-s`）/ **default 16**（`-l`）/ l 24（`-xl`） |
| 字号 | default & sm 14、lg 16（`contentFontSize` ?? `fontSize`） | mini 12（body-1）、small/default/large **14**（body-3） | s 12（body-small）/ **default 14**（body-medium）/ l 16（body-large） |
| 字重 | **400**（`prepareComponentToken`） | **400**（`@btn-font-weight: @font-weight-400`） | 未在 token 定义（默认 400） |
| 圆角 | default **6** / lg 8 / sm 4（`borderRadius` 系列） | 全档 **2**（`@btn-border-radius: @radius-small`） | 全档 **3**（`@btn-border-radius: @border-radius-default` = `--td-radius-default`）；shape=round 时 `calc(高/2)` |
| 主色 | `#1677ff`（`colorPrimary`） | `#165dff`（`@color-primary-6` = arcoblue-6） | `#0052d9`（`@brand-color` = brand-7） |
| hover / active | `colorPrimaryHover`(#4096ff) / `colorPrimaryActive`(#0958d9)（派生色阶） | primary-5 / primary-7（色阶查表） | brand-6(#366ef4) / brand-8(#003cab)（色阶查表） |

出处：
- Ant：`components/theme/themes/seed.ts`（controlHeight/fontSize/borderRadius/lineWidth）、`components/button/style/token.ts`（`prepareComponentToken`：fontWeight 400、paddingInline、contentFontSize）、`components/button/style/index.ts`（`genSizeStyle`：sm/lg 换 controlHeightSM/LG、borderRadiusSM/LG）
- Arco：`components/Button/style/token.less`（`@btn-size-*-height/padding-horizontal/font-size`、`@btn-border-radius`）
- TDesign：`style/web/components/button/_var.less`（`@btn-height-*`、`@btn-padding-horizontal-*`、`@btn-border-radius`、状态色）

## 2. 输入框 / 选择器

| 维度 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| 高度 | sm 24 / **default 32** / lg 40 | mini 24 / small 28 / **default 32** / large 36 | s 24 / **default 32** / l 40（input 与 select 同一套） |
| 水平 padding | default & lg **11**（`paddingSM(12)−1`）、sm 7（`controlPaddingHorizontalSM(8)−1`） | mini 8 / small 12 / **default 12** / large 16（`@input-*-padding-horizontal` = spacing-4/6/6/7） | **default `0 8px`**（`@input-padding-default: 0 @comp-paddingLR-s`）；l 档 `0 12px` |
| 圆角 | default **6** / lg 8 / sm 4 | **2**（`@input-border-radius: @radius-small`） | **3**（`@input-border-radius: @border-radius-default`） |
| 默认边框 | 1px `colorBorder`（= 白基色加深 15% → `#d9d9d9`） | **默认无描边**：border 全档 `transparent`，靠灰底 `fill-2` 表意 | 1px `border-level-2-color` |
| 默认背景 | `colorBgContainer`（白） | `fill-2`（灰底），focus 时换 `bg-2`（白） | `bg-color-specialcomponent`（浅色主题下白） |
| hover 边框 | `colorPrimaryHover` | 保持 transparent（hover 换底色 fill-3） | 变 `brand-color` |
| **focus 态** | 边框 `colorPrimary` + `boxShadow: 0 0 0 2px controlOutline`（主色浅底 alpha 混合）；错误态换 `colorErrorOutline` | 边框 `color-primary-6` + 底色变白 + 无外圈阴影（`@input-size-shadow_focus: @shadow-distance-none`） | 边框 `brand-color` + `box-shadow: 0 0 0 2px @brand-color-focus`（= `--td-brand-color-2`，`#d9e1ff`） |
| placeholder | `colorTextQuaternary`（黑 25% alpha） | `color-text-3` | `text-color-placeholder` |
| 字号 | 14 / sm 12 / lg 16（`inputFontSize*` ?? fontSize 系列） | default 14（body-3）、mini 12 | default 14（body-medium）、s 12、l 16 |

出处：
- Ant：`components/input/style/token.ts`（`initInputToken`/组件默认：paddingInline、activeBorderColor、activeShadow `0 0 0 2px`、hoverBorderColor）、`components/theme/themes/default/colors.ts`（colorBorder=白+15% 深）、`components/theme/util/alias.ts`（paddingSM/controlPaddingHorizontal）
- Arco：`components/Input/style/token.less`（边框/背景/focus 全表、尺寸、圆角、布局）
- TDesign：`style/web/components/input/_var.less`（边框色、focus box-shadow、padding、高度）、`select/_var.less`（高度同表）

## 3. 复选框 / 单选 / 开关

### 复选框 Checkbox

| 维度 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| 尺寸 | **16**（`controlInteractiveSize = controlHeight/2`） | **14**（`@checkbox-mask-height`）；hover 热区 24（`@checkbox-mask-bg-height: @size-6`） | **16**（`@checkbox-size: 16px`） |
| 边框 | 1px `colorBorder`，选中 1px `colorPrimary` | **2px**（`@checkbox-mask-border-width: @border-2`），选中边框 transparent | 1px `border-level-2-color`，选中变 `brand` |
| 圆角 | 4（`borderRadiusSM`） | 2（`@radius-small`） | 3（`@border-radius-default`） |
| 选中色 | bg+border 均 `colorPrimary`，对勾白 | bg `@color-primary-6`，对勾白 | bg `@brand-color`，对勾白（勾 5×9px） |
| hover | 边框 `colorPrimary` | 边框 `fill-4`（中性） | 边框 `brand` |
| 半选 | bg `colorBgContainer` + 中性边框，短横线 `colorPrimary` | bg `@color-primary-6` + 白色短横 | bg `@brand-color` + 白色短横 |

### 单选 Radio

| 维度 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| 尺寸 | **16**（`radioSize = fontSizeLG`） | **14**（`@radio-layout-height`）；热区 24 | **16**（`@radio-size`），内点 8（`/2`） |
| 形状 | 圆 | 圆（`@radius-circle`） | 圆 |
| 选中 | 内圆 `colorPrimary`（默认非 wireframe：外圈 `colorPrimary` 底+白点） | 外圈 bg `@color-primary-6`，内点白 | 外圈边框变 `brand`，内点 `brand` |
| 按钮型高度 | 沿用 controlHeight 档位 | `@radio-size-*-height` = 24/28/32/36 同按钮 | medium `calc(32 − 2×2) = 28`，圆角 2 |

### 开关 Switch

| 维度 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| 默认高度 | **22**（`fontSize×lineHeight = 14×1.5714`，公式派生） | **24**（`@switch-size-default: @size-6`） | **20**（`--td-comp-size-xxs`），s 档 16、l 档 24 |
| 默认最小宽 | 44（`handleSize×2 + padding×4 = 18×2+8`）；sm 28 | 40（circle 型 `@size-10`；line 型宽 36） | `calc(高 / 0.618)` ≈ **32.4**（黄金比） |
| 手柄 | 18 / sm 12，白底 | 16 / sm 12，白底 | 白底（宽度由 border 值推导） |
| 选中色 | `colorPrimary` | `@color-primary-6` | `@brand-color` |
| 未选中色 | 中性灰 | `fill-4` | `bg-color-secondarycomponent` |

出处：
- Ant：`components/checkbox/style/index.ts`（尺寸/borderRadiusSM/checked）、`components/radio/style/index.ts`（`prepareComponentToken`: radioSize=fontSizeLG）、`components/switch/style/index.ts`（trackHeight/handleSize 公式）、`components/theme/util/alias.ts`（controlInteractiveSize=controlHeight/2）
- Arco：`components/Checkbox/style/token.less`、`components/Radio/style/token.less`、`components/Switch/style/token.less`
- TDesign：`style/web/components/checkbox/_var.less`、`radio/_var.less`、`switch/_var.less`

## 4. 弹窗 Modal

| 维度 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| 默认宽度 | **520**（`Modal.tsx` `width = 520`；Confirm 弹窗 416） | **520**（`@modal-default-size-width`）；simple 型 464 | **480**（`@dialog-width: 480px`） |
| 圆角 | **8**（`borderRadiusLG`） | **4**（`@modal-border-radius: @radius-medium`） | **6**（`@dialog-border-radius: @border-radius-medium`） |
| 内边距（非 wireframe/默认型） | 内容 `20px 24px`（`paddingMD` × `paddingContentHorizontalLG`），header padding 0 + 下间距 8（`marginXS`），footer 上间距 12（`marginSM`） | 水平 **20**（`@spacing-8`），header 高 48，内容上下 24（`@spacing-9`），footer 上下 16（`@spacing-7`） | 整体 spacer **32×32**（`@comp-paddingTB-xxl @comp-paddingLR-xxl`），body 上下 16，footer 上 16 |
| 标题字号 | 16（`fontSizeHeading5`） | 16（`@font-size-title-1`）**字重 500** | 16（`@font-title-medium`）**字重 600** |
| 正文字号 | 14（`fontSize`） | 14（`@font-size-body-3`） | 14（`@font-body-medium`） |
| 遮罩 | `colorBgMask` = **rgba(0,0,0,0.45)** | rgba(gray-10 `#1d2129`, **60%**）（`@mask-color-bg`） | **rgba(0,0,0,60%)**（`--td-mask-active`） |
| 边框/阴影 | 无边框 + `boxShadow`（三层投影）；`contentBg: colorBgElevated` | 无边框无阴影（`@modal-border-width: @border-none`、`@modal-box-shadow: @shadow-none`），靠遮罩分层 | 1px `border-level-1-color` |
| 位置 | 垂直居中（v5 默认 centered） | 距顶 100px（`@modal-margin-top`） | 距顶 20vh（`@dialog-top-position-top`） |
| zIndex | 1000（`zIndexPopupBase`） | 1001 | popup 体系（`--td-z-index-popup` 6000 档，popup 组件独立） |

出处：
- Ant：`components/modal/style/index.ts`（`prepareComponentToken`：contentPadding/headerPadding/titleFontSize/mask）、`components/modal/Modal.tsx`（width=520）、`components/modal/ConfirmDialog.tsx`（416）、`components/theme/themes/shared/genColorMapToken.ts`（colorBgMask=0.45）
- Arco：`components/Modal/style/token.less`（宽度/圆角/padding 全表）、`components/Modal/style/index.less`（mask 色）、`components/style/theme/global.less`（`@mask-color-bg`）
- TDesign：`style/web/components/dialog/_var.less`（宽度/圆角/spacer/字体/遮罩全表）

## 5. 分段控件 / Tabs

> Arco、TDesign 无独立 Segmented 组件；Arco 的 Tabs capsule 型、TDesign 的 segmented 类组件共用 Tabs 尺寸表，以 Tabs 为准对照。AntD 两个都有，分别列出。

### Ant Design Segmented（独有）

| 维度 | 值 |
|---|---|
| item 高度 | default **28**（`controlHeight − trackPadding×2 = 32−4`）、sm 20、lg 36 |
| item 水平 padding | default **11**（`controlPaddingHorizontal(12) − lineWidth`）、sm 7 |
| 圆角 | 轨道 6（`borderRadius`）、sm 4、lg 8 |
| 轨道/选中 | 轨道底 `colorBgLayout`、选中底 `colorBgElevated`、选中字 `colorText`；track padding `lineWidthBold`=2 |

出处：`components/segmented/style/index.ts`（labelHeight 计算 + `prepareComponentToken`）

### Tabs / 分段 三家对照

| 维度 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| 高度 | card 型 **40**（`cardHeight = controlHeightLG`）、sm 32、lg 48 | line 型 **40**（`@size-10`）、card/capsule 型 **32**（`@size-8`）、large 档 44 | middle **48**（`--td-comp-size-xxl`）、large **64**；nav item 内容高 32 |
| item padding | 水平 `12px 0`（`paddingSM`）、lg `16px 0`、sm `8px 0` | 标题水平 **8**（`@spacing-4`）、line 型 **16**、card 型 16、capsule 12 | `0 8px`（large 档 `0 12px`） |
| 选中态 | 字色 `colorPrimary`；line 型底部 2px ink bar（`colorPrimary`） | 字色 `@color-primary-6` + 字重 **500**（`@font-weight-500`）；ink bar `@color-primary-6` | 字色 `@brand-color`；ink bar **3px** `@brand-color` |
| 圆角 | 卡片型用 `borderRadius` | 全型 **2**（`@radius-small`） | 未单列（跟随全局） |
| 未选中字色 | `colorText` | `color-text-2` | `text-color-secondary` |

出处：
- Ant：`components/tabs/style/index.ts`（`prepareComponentToken`：cardHeight、horizontalItemPadding、itemColor/itemSelectedColor、inkBarColor）
- Arco：`components/Tabs/style/token.less`（`@tabs-size-*-header-height_*`、padding、active 字色/字重、ink bar）
- TDesign：`style/web/components/tabs/_var.less`（`@tab-height-*`、`@tab-default-stroke-size: 3px`、选中色）

## 6. 全局体系

### 控件高度体系

| 档位语义 | Ant Design（公式） | Arco Design（静态表） | TDesign（CSS 变量表） |
|---|---|---|---|
| 特小 | 16（`controlHeightXS = ×0.5`） | mini 24 | `--td-comp-size-xxxs` 16 |
| 小 | 24（`controlHeightSM = ×0.75`） | small 28 | `--td-comp-size-xs` 24 |
| **默认** | **32**（`controlHeight`，seed 显式值） | **32**（`@size-default`） | **32**（`--td-comp-size-m`） |
| 大 | 40（`controlHeightLG = ×1.25`） | large 36 | `--td-comp-size-xl` 40 |
| 更大档 | —（无） | `@size-10` 40 … `@size-50` 200（4px 步进通用尺寸表） | `--td-comp-size-xxl` 48 … `xxxxxl` 72（8px 步进） |

出处：Ant `components/theme/themes/seed.ts` + `themes/shared/genControlHeight.ts`；Arco `components/style/theme/global.less`（`@size-*`、`@size-mini/small/default/large`）；TDesign `style/web/theme/_size.less`。

### 圆角体系

| 档位 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| base/默认 | 6（seed `borderRadius`） | 4（`@border-radius-medium`） | 3（`--td-radius-default`） |
| 小 | 4（`borderRadiusSM`，派生：base=6 → 4） | 2（`@border-radius-small`） | 2（`--td-radius-small`） |
| XS | 2（`borderRadiusXS`） | — | — |
| 大 | 8（`borderRadiusLG`，派生：base∈[6,16) → base+2） | 8（`@border-radius-large`） | 9（`--td-radius-large`）/ 12（extraLarge） |
| 圆形 | `50%`（各组件自用） | `@border-radius-circle: 50%` | `--td-radius-circle: 50%` / round `999px` |
| 派生规则 | **算法派生**：`genRadius(radiusBase)` 按 base 区间推导 SM/XS/LG/Outer（改 seed 自动联动） | **静态四档**（0/2/4/8/50%） | **静态五档 + round**（2/3/6/9/12/999px/50%） |

出处：Ant `components/theme/themes/seed.ts` + `themes/shared/genRadius.ts`；Arco `components/style/theme/global.less`；TDesign `style/web/theme/_radius.less`。

### 字号与主色（控件相关全局）

| 项 | Ant Design | Arco Design | TDesign |
|---|---|---|---|
| 正文字号 | 14（seed） | 14（`@font-size-body-3`） | 14（`--td-font-size-body-medium`） |
| 小/大字号 | 12 / 16（genFontSizes 算法） | 12 / 16（body-1 / title-1） | 12 / 16（body-small / body-large） |
| 主色 | `#1677ff` | `#165dff`（arcoblue-6） | `#0052d9`（brand-7） |
| focus 描边宽 | `lineWidthFocus` = **3**（`lineWidth×3`，`focusOutline: true` 时） | focus-visible shadow 半径 2 | focus 外圈 **2px**（box-shadow） |

---

## 三家共识

1. **默认控件高度 32px**：三家的 default 档全部锚定 32（Ant seed 显式值、Arco `@size-default`、TDesign `--td-comp-size-m`），且小档 24–28、大档 36–40 收拢在同一区间。
2. **默认正文 14px、按钮字重 400、选中态主色+白字**：按钮/输入框字号 default 全是 14，只有大档升 16；按钮字重 Ant/Arco 显式 400；复选框/单选/开关选中色三家全部用主色。
3. **输入框 focus = 「边框变主色 + 2px 浅主色外圈」**：AntD（`0 0 0 2px controlOutline`）与 TDesign（`0 0 0 2px brand-color-focus`）是同构做法，外圈都是主色浅阶（低饱和/高亮度），宽度同为 2px。
4. **Modal 宽 480–520、圆角 4–8、遮罩 45–60% 黑**：宽度 520(Ant/Arco)/480(TDesign)；遮罩三家都是半透明黑（0.45/0.6/0.6）；标题三家都是 16px。
5. **档位换算节奏 ~8px**：小档比默认低 8（Arco/TDesign）或 25%（AntD），大档比默认高 8（AntD/TDesign）或 12.5%（Arco）。

## 分歧点

1. **默认圆角**：AntD 6（且算法联动派生 2/4/8）vs Arco 控件普遍用 2（按钮/输入框 `radius-small`，Modal 才用 4）vs TDesign 3（全控件 `radius-default`）——同为「中文中后台」审美下圆角从 2 到 6 差 3 倍，是三家最大的分歧。
2. **输入框默认形态**：Arco 无边框灰底（fill 系）vs AntD/TDesign 描边白底——Arco 把「边界感」交给底色。
3. **focus 态机制**：AntD v5 键盘 focus 用 `:focus-visible` **outline 3px**（`lineWidthFocus`），鼠标 focus 不画外圈（按钮靠边框色变化）；Arco 仅 focus-visible 时给 2px 阴影、输入框 focus 连外圈都没有（只换边框色）；TDesign 鼠标+键盘统一 2px box-shadow 外圈。
4. **控件高度体系结构**：AntD 是「seed + 乘法公式」（改 32 全体系联动）；Arco/TDesign 是静态档位表，且 Arco 比 TDesign 多一档 mini/small 区分（24/28 都有小档）。
5. **复选框尺寸与边框**：16px(Ant/TDesign) vs 14px(Arco)；选中态边框宽 1px(Ant/TDesign) vs 2px(Arco)。
6. **开关默认高度**：22(AntD，行高派生) / 24(Arco) / 20(TDesign)，最小宽 AntD 用手柄推导 44px、TDesign 用黄金比 `高/0.618`、Arco 固定 40px——开关是三家规格最不齐的控件。
7. **Tabs 高度**：TDesign 明显偏大（middle 48 / large 64，字 16px），AntD 40、Arco line 40；TDesign 的 ink bar 3px 也比 AntD 的 2px 厚。
