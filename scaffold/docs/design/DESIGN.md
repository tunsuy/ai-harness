---
# 项目填写：Stitch 兼容 YAML tokens（colors / typography / spacing / radii / …）
# 例见 VoltAgent/awesome-design-md 与 Google DESIGN.md 规范。
# 本文件是本仓视觉 SSOT；参照库只影响当轮原型，晋升才改这里。
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

## Do's and Don'ts

### Don't（常见引擎级红线，可删改）

- Don't invent hex outside this file.
- Don't ship purple/lavender/magenta gradient defaults or multi-accent KPI walls.
- Don't copy marketing mesh / cream hero as the product default unless Brief 明确要营销页。

## References

上游灵感：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)；本地取法：[references/README.md](./references/README.md)。  
本文件是 **本仓合成**，不是品牌官方规范拷贝。
