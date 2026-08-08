# Greenthink · 你的创意，应该被看见

> 世界上从不缺少好想法，只缺少让它们被看见的地方。

> 🌐 [English](README.en.md) | 中文

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/qq1262580454-a11y/greenthink?style=social)](https://github.com/qq1262580454-a11y/greenthink)

> 📜 我们的信念与承诺，见 [《开源宣言》](OPEN-SOURCE-MANIFESTO.md)

---

## 这不是一个程序，这是一个理念

这个时代，AI 让每个人都拥有了创造的能力。

但绝大多数创作者正在「埋头造车」——沉迷参数、调试模型、打磨提示词，把热情全部花在「怎么生成」上。而那些真正做出来的、完整而成熟的成果，却常常躺在本地文件夹里，从未被第二个人看见。

**Greenthink，是让 AI 成果被看见的展示平台。**

- 我们不展示创作过程，只呈现最终创意结果
- 我们收纳：完整、成熟、最终的创意成果，以及它背后的思想与世界观
- 我们相信：

> **想法大于参数 · 创意大于技巧 · 结果大于过程 · 想象力大于工具**

## 平台是什么

一个任何人都能提交、展示、发现 AI 创意成果的地方：

| 你能做 | 怎么发生 |
|---|---|
| 🎨 提交你的完整成果 | 一个作品、一套方案、一个工具，几分钟完成提交 |
| 👀 发现别人的创意 | 在展厅里浏览，每个成果都有完整故事 |
| 📖 读懂每个成果 | 问题 → 创意解法 → 最终结果，三段式呈现 |
| ✅ 让好内容浮现 | 管理员审核把关，保证每个上线的成果都完整成熟 |

## 让理念运转起来

**给创作者：** 打开网站 → 「提交创意」→ 审核通过 → 你的成果被看见。

**给共建者：** 代码只是载体，理念需要人——
创作者提交成果，设计师打磨视觉，开发者提 PR，传播者把它分享给正在埋头造车的朋友。

## 技术附录（给开发者）

- **技术栈**：Flask + 原生 HTML/CSS/JS，零构建，双击能跑
- **本地运行**：`pip install flask && python app.py` → http://127.0.0.1:5010
- **数据**：`data/results.json`，一份公开的 JSON，谁都能验证
- **配图**：`static/img/works/<成果id>.jpg`（4:3，有图自动显示）
- **参与开发**：[CONTRIBUTING.md](CONTRIBUTING.md) · 认领 `good first issue`
- **协议**：[MIT License](LICENSE)

---

> 工具交给AI迭代，想象力由人类定义。
>
> 让每一个藏在脑海里的创意，终于有地方落地、被看见、被记住。
