# 贡献指南

欢迎参与 Greenthink！无论你是想提交创意成果、配图、还是写代码，都感谢你的贡献。

## 🎨 内容贡献（不需要写代码）

1. **提交作品**：打开网站 → 「提交作品」→ 填写表单 → 管理员审核通过后展示
2. **配图**：把封面图放到 `static/img/works/<成果id>.jpg`（4:3，800×600 以上）
3. **文案**：作品简介要讲清楚"它解决了什么问题、最终结果是什么"

## 💻 代码贡献

### 环境准备
```bash
git clone <仓库地址>
pip install flask
python app.py    # http://127.0.0.1:5010
```

### 提 PR 流程
1. 先开 Issue 说明你要做什么（避免撞车）
2. Fork 仓库，新建分支：`git checkout -b feat/xxx`
3. 改动 + 自测（至少跑通 `python app.py` 和相关页面）
4. 提交 PR，描述清楚改了什么、为什么

### 代码约定
- Flask + 原生 HTML/CSS/JS，**不要引入前端框架**（保持零构建、双击能跑）
- 风格保持全站统一（`static/style.css` 顶部有配色注释）
- 数据存 `data/results.json`，改结构时注意向后兼容
- 图片一律放 `static/img/works/`，命名用成果 id

### 认领任务
- 看 Issues 里标了 `good first issue` 的任务开始
- 不确定怎么做？先评论问，或直接开 Issue 讨论

## 📋 提交信息规范

```
feat: 新增 XX 功能
fix: 修复 XX 问题
docs: 更新文档
style: 样式调整
```

## ⚠️ 注意

- 审核是唯一入口：内容请走平台提交，不要直接改 `results.json` 上线
- 动模板后必须重启服务才生效（Flask debug=False 模板缓存）
