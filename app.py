# -*- coding: utf-8 -*-
"""Greenthink —— 你的创意，应该被看见
Flask + JSON 存储：官网首页 / 成果展厅 / 作品详情 / 提交 / 管理（审核）
中英双语（i18n）· 端口 5010
"""
import json
import os
import threading
from datetime import date

from flask import Flask, abort, redirect, render_template, request, session, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "results.json")
IMG_DIR = os.path.join(BASE_DIR, "static", "img", "works")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")
LOCK = threading.Lock()

app = Flask(__name__)
app.secret_key = "greenthink-creative-showcase"
app.json.sort_keys = False

# ═══════════ 界面文案（中/英） ═══════════
UI = {
    "zh": {
        "nav_works": "展厅", "nav_submit": "提交作品", "nav_creators": "创作者",
        "nav_about": "关于我们", "nav_cta": "提交创意",
        "hero_h1": "你的创意，应该被看见",
        "hero_intro": "世界上从不缺少好想法，只缺少让它们被看见的地方。",
        "btn_browse": "浏览展厅", "btn_submit": "提交作品",
        "featured": "精选创意成果", "view_all": "查看全部成果",
        "footer_h2a": "让每一个藏在脑海里的创意，",
        "footer_h2b": "终于有地方落地、被看见、被记住。",
        "footer_tag": "工具交给AI迭代，想象力由人类定义。",
        "works_title": "成果展厅",
        "works_sub": "共 {n} 个成果 · 我们不展示创作过程，只呈现最终创意结果",
        "works_empty": "该分类下暂无成果，来提交第一个",
        "work_back": "← 返回展厅", "work_creator": "创作者", "work_views": "次被看见",
        "work_try": "▶ 体验这个成果",
        "work_problem": "遇到的问题", "work_solution": "创意的解法", "work_result": "最终结果",
        "work_cta": "你也做出了成果？提交你的作品，让更多人看见。",
        "submit_title": "提交你的创意成果",
        "submit_sub": "不要求会写代码。只要你用AI做出了<b>完整、成熟、最终的创意成果</b>——一个作品、一套方案、一个工具都行。提交后经管理员审核，就会展示在展厅里。",
        "form_title": "成果名称", "form_author": "创作者署名", "form_industry": "所属领域",
        "form_tag": "分类", "form_summary": "一句话简介", "form_problem": "它解决了什么问题",
        "form_solution": "创意是怎么落地的", "form_result": "最终结果",
        "form_effects": "效果数据（每行一条）", "form_link": "体验链接（选填）",
        "submit_btn": "提交成果", "browse_btn": "先逛逛展厅",
        "submit_ok": "✅ 提交成功", "submit_ok_sub": "你的创意成果已进入审核队列，通过后会展示在展厅里。",
        "admin_title": "成果管理", "admin_pending": "⏳ 待审核", "admin_online": "🟢 已上线",
        "admin_preview": "预览", "admin_approve": "通过", "admin_delete": "删除",
        "n404_title": "404", "n404_sub": "这个页面不存在，回展厅看看吧。", "n404_btn": "回首页",
        "lang": "EN",
    },
    "en": {
        "nav_works": "Gallery", "nav_submit": "Submit Work", "nav_creators": "Creators",
        "nav_about": "About", "nav_cta": "Submit Idea",
        "hero_h1": "Your creativity deserves to be seen",
        "hero_intro": "The world never lacks good ideas — it lacks places where they can be seen.",
        "btn_browse": "Browse Gallery", "btn_submit": "Submit Work",
        "featured": "Featured Creations", "view_all": "View All Creations",
        "footer_h2a": "Every idea hidden in someone's mind,",
        "footer_h2b": "finally has a place to land, be seen, and be remembered.",
        "footer_tag": "Tools evolve with AI; imagination is defined by humans.",
        "works_title": "Creation Gallery",
        "works_sub": "{n} creations · We show final results, not the process",
        "works_empty": "No creations in this category yet — submit the first one",
        "work_back": "← Back to Gallery", "work_creator": "Creator", "work_views": "views",
        "work_try": "▶ Experience this work",
        "work_problem": "The Problem", "work_solution": "The Creative Solution", "work_result": "The Final Result",
        "work_cta": "Made something too? Submit your work and let it be seen.",
        "submit_title": "Submit Your Creation",
        "submit_sub": "No coding required. If you made a <b>complete, mature, final creative work</b> with AI — a piece, a plan, a tool — submit it. It will appear in the gallery after review.",
        "form_title": "Work Title", "form_author": "Creator Name", "form_industry": "Field / Industry",
        "form_tag": "Category", "form_summary": "One-line Summary", "form_problem": "What problem does it solve",
        "form_solution": "How the idea came to life", "form_result": "The final result",
        "form_effects": "Impact metrics (one per line)", "form_link": "Experience link (optional)",
        "submit_btn": "Submit Work", "browse_btn": "Browse Gallery",
        "submit_ok": "✅ Submitted", "submit_ok_sub": "Your creation is in the review queue and will appear in the gallery once approved.",
        "admin_title": "Manage Creations", "admin_pending": "⏳ Pending Review", "admin_online": "🟢 Live",
        "admin_preview": "Preview", "admin_approve": "Approve", "admin_delete": "Delete",
        "n404_title": "404", "n404_sub": "This page does not exist. Head back to the gallery.", "n404_btn": "Back to Home",
        "lang": "中文",
    },
}

# 分类（value, 中文, 英文）
TAGS = [
    ("全部", "全部", "All"),
    ("设计创意", "设计创意", "Creative Design"),
    ("效率工具", "效率工具", "Productivity"),
    ("办公自动化", "办公自动化", "Office Automation"),
    ("文档生成", "文档生成", "Document Generation"),
    ("数据分析", "数据分析", "Data Analysis"),
    ("其他", "其他", "Other"),
]
TAG_VALUES = [t[0] for t in TAGS]


def load_results():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["results"]


def save_results(results):
    with LOCK:
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"results": results}, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DATA_FILE)


def next_id(results):
    return max((r["id"] for r in results), default=0) + 1


def online_list(results):
    return [r for r in results if r["status"] == "online"]


def attach_img(results):
    """成果 id 对应 static/img/works/<id>.jpg(.png/.webp)，存在则标记 has_img"""
    for r in results:
        r["has_img"] = any(
            os.path.exists(os.path.join(IMG_DIR, f"{r['id']}{ext}"))
            for ext in IMG_EXTS
        )
    return results


def lang_of():
    return session.get("lang", "zh") if session.get("lang") in UI else "zh"


def ctx(**kw):
    """每个页面通用的语言上下文"""
    lang = lang_of()
    kw["lang"] = lang
    kw["T"] = UI[lang]
    return kw


@app.route("/lang/<code>")
def set_lang(code):
    if code in UI:
        session["lang"] = code
    return redirect(request.referrer or url_for("home"))


@app.route("/")
def home():
    results = load_results()
    featured = attach_img(online_list(results))[:3]
    total = len(online_list(results))
    views = sum(r.get("views", 0) for r in online_list(results))
    inds = len(set(r["industry"] for r in online_list(results)))
    return render_template("home.html", featured=featured,
                           total=total, views=views, inds=inds, active="home",
                           **ctx())


@app.route("/works")
def works():
    results = load_results()
    results = attach_img(results)
    tag = request.args.get("tag", "全部")
    tag = tag if tag in TAG_VALUES else "全部"
    shown = [r for r in online_list(results) if tag == "全部" or r["tag"] == tag]
    return render_template("works.html", results=shown, tags=TAGS, cur=tag,
                           total=len(online_list(results)), active="works",
                           **ctx())


@app.route("/work/<int:rid>")
def work(rid):
    results = load_results()
    results = attach_img(results)
    r = next((x for x in results if x["id"] == rid), None)
    if not r:
        abort(404)
    r["views"] = r.get("views", 0) + 1
    save_results(results)
    return render_template("work.html", r=r, active="", **ctx())


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        f = request.form
        title = (f.get("title") or "").strip()
        author = (f.get("author") or "").strip()
        summary = (f.get("summary") or "").strip()
        if not title or not author:
            return render_template("submit.html", tags=TAGS, err="成果名称和创作者必填 / Title and creator are required",
                                   active="submit", **ctx())
        results = load_results()
        results.append({
            "id": next_id(results),
            "title": title,
            "author": author,
            "industry": (f.get("industry") or "").strip() or "Other",
            "tag": f.get("tag") if f.get("tag") in TAG_VALUES else "其他",
            "summary": summary,
            "problem": (f.get("problem") or "").strip(),
            "solution": (f.get("solution") or "").strip(),
            "result": (f.get("result") or "").strip(),
            "effects": [x.strip() for x in (f.get("effects") or "").splitlines() if x.strip()],
            "link": (f.get("link") or "").strip(),
            "status": "pending",
            "views": 0,
            "created": date.today().isoformat(),
        })
        save_results(results)
        return redirect(url_for("submit_done"))
    return render_template("submit.html", tags=TAGS, err="", active="submit", **ctx())


@app.route("/submit/done")
def submit_done():
    return render_template("submit_done.html", active="", **ctx())


@app.route("/admin")
def admin():
    results = load_results()
    pending = [r for r in results if r["status"] == "pending"]
    online = online_list(results)
    return render_template("admin.html", pending=pending, online=online, active="", **ctx())


@app.route("/admin/approve/<int:rid>", methods=["POST"])
def approve(rid):
    results = load_results()
    for r in results:
        if r["id"] == rid:
            r["status"] = "online"
            break
    save_results(results)
    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:rid>", methods=["POST"])
def delete(rid):
    results = load_results()
    results = [r for r in results if r["id"] != rid]
    save_results(results)
    return redirect(url_for("admin"))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", **ctx()), 404


if __name__ == "__main__":
    print("Greenthink 启动: http://127.0.0.1:5010")
    app.run(host="0.0.0.0", port=5010, debug=False)
