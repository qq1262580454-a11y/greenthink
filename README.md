# Greenthink · 你的创意，应该被看见

> 世界上从不缺少好想法，只缺少让它们被看见的地方。

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-lightblue)](https://flask.palletsprojects.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/qq1262580454-a11y/greenthink?style=social)](https://github.com/qq1262580454-a11y/greenthink)
[![Issues](https://img.shields.io/github/issues/qq1262580454-a11y/greenthink)](https://github.com/qq1262580454-a11y/greenthink/issues)

> 📜 我们的信念与承诺，见 [《开源宣言》](OPEN-SOURCE-MANIFESTO.md)

Greenthink 是一个**创意成果展示平台**：我们不展示创作过程，只呈现最终创意结果。
任何人都可以提交自己用 AI 做出的完整创意成果——一个作品、一套方案、一个工具——
让创意被看见、被记住。

## ✨ 功能

- **官网首页**（`/`）：品牌理念 + 精选创意成果
- **成果展厅**（`/works`）：全部成果卡片 + 分类筛选
- **作品详情**（`/work/<id>`）：问题 → 创意解法 → 最终结果 三段式叙事
- **提交作品**（`/submit`）：任何人提交创意成果，进入审核队列
- **管理后台**（`/admin`）：审核通过 / 删除

## 🚀 本地运行

```bash
pip install flask
python app.py
```

打开 http://127.0.0.1:5010

> 也可以直接双击 `启动工具.bat`（Windows）。

## 📁 目录结构

```
AI成果展/
├── app.py                 # Flask 主程序（全部路由）
├── data/results.json      # 成果数据（JSON，改完刷新即生效）
├── templates/             # 页面模板
├── static/
│   ├── style.css          # 全站样式
│   ├── main.js            # 滚动淡入
│   └── img/works/         # 作品封面图（1.jpg / 2.jpg …对应成果 id）
└── 启动工具.bat / 停止工具.bat
```

## 🖼 给作品配图

把图片放到 `static/img/works/<成果id>.jpg`（支持 jpg/png/webp），
有图自动显示，无图自动回退渐变占位。建议 4:3，800×600 以上。

## 🤝 如何参与

**不想写代码？照样能贡献：**
- 用平台提交你的创意成果——这是最重要的贡献
- 帮忙配图、写作品文案、传播分享

**会写代码？欢迎提 PR：**
- 新功能、修 bug、优化样式，流程见 [CONTRIBUTING.md](CONTRIBUTING.md)
- 认领任务请先开 Issue 讨论，避免重复劳动

## 📄 协议

MIT License —— 自由使用、修改、分发。
