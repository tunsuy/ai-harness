# 设计参照库（references）

> 用途：设计任务（原型闸轮次 / 新页面 / 重设计）前的**参照系**输入——agent 缺少「见过好设计」的锚点，从这里取。  
> 来源：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)（MIT · 多品牌 DESIGN.md 文字设计系统 · Google Stitch [DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) 约定）

## 取法

**品牌文件直接落库**（`awesome-design-md/<brand>/DESIGN.md`，上游 LICENSE 随附）——换机器 / 新 clone 免拉取，每个品牌的网络成本只付一次。目录随轮次有机生长：当轮需要哪个品牌，拉完提交进库。

脚手架默认带 **stripe** 首份样例；其它品牌按需追加。

```bash
# 新增品牌 / 刷新（主力：jsDelivr fastly 节点）
curl -sL "https://fastly.jsdelivr.net/gh/VoltAgent/awesome-design-md@main/design-md/<brand>/DESIGN.md" \
  -o docs/design/references/awesome-design-md/<brand>/DESIGN.md
#   备用链（依次降级）：fastly.jsdelivr.net → cdn.jsdelivr.net → raw.githubusercontent.com
#   不用第三方 GitHub 代理（gh-proxy 等）：内容可被篡改且不可校验
#   拉完提交进库；刷新时 git diff 即上游变化

# 品牌目录（选老师前先看有什么；库里已有哪些先翻本地）
curl -s "https://api.github.com/repos/VoltAgent/awesome-design-md/contents/design-md" | grep '"path"'

# 整库离线包（很少需要；勿用 git clone——慢一个数量级）
curl -sL "https://codeload.github.com/VoltAgent/awesome-design-md/tar.gz/refs/heads/main" | tar xz
```

## 用法（每轮设计时做，不预存结论）

**本目录不维护「页面部分 → 品牌」对照表**——页面结构每轮会变，参照选择跟着当轮设计走，记录在当轮 feature 文档里：

1. 列出**这一轮**页面要画的部分（从当轮 brief / prototype 出发）；
2. 每部分提一个具体问题（例：「谁把代码接入卡画得最好」），从品牌目录挑 1–2 个老师；
3. 带着问题读对应 DESIGN.md，只看和问题相关的章节；
4. 把「问题 → 老师 → 学到什么」写进当轮 `prototype.md` 的设计约束段（显式记录，人闸可审可否决）。

## 纪律

- **学模式，不搬值**：学字阶比例、间距节奏、阴影语法、组件状态的克制程度；参照品牌的 hex / 字体 / logo 语言一律不进本仓 [`DESIGN.md`](../DESIGN.md) token 体系（SSOT 唯一）。
- **品牌不能整学**：每家都有项目禁的东西（例：多色 mesh 渐变）。读任何品牌都限定在当轮问题范围内；禁区写在本仓 DESIGN.md / product-pipeline。
- **单源存疑要核对**：库内容是第三方 "inspired interpretation"（非品牌官方规范）。关键事实拿不准时：双通道交叉核对（jsDelivr 与 raw 各拉一份 `diff`）、本地截图核对、或提请产品负责人判断；仲裁结论回写本文件。
- **晋升只走本仓 DESIGN.md**：某条经验反复验证有效，才并入项目 `DESIGN.md`；在此之前参照只影响当轮原型。
- **归属**：上游 MIT，LICENSE 随库；`awesome-design-md/` 内文件系上游原样拷贝，勿手改（重拉即覆盖）；不得声称品牌官方规范，不进对外物料。
