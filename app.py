# -*- coding: utf-8 -*-
"""Greenthink —— 你的创意，应该被看见
Flask + JSON 存储：官网首页 / 成果展厅 / 作品详情 / 提交 / 管理（审核）
端口 5010
"""
import json
import os
import threading
from datetime import date

from flask import Flask, abort, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "results.json")
IMG_DIR = os.path.join(BASE_DIR, "static", "img", "works")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")
LOCK = threading.Lock()

app = Flask(__name__)
app.json.sort_keys = False  # 保持 jsonify 字段顺序


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


TAGS = ["全部", "设计创意", "效率工具", "办公自动化", "文档生成", "数据分析", "其他"]


@app.route("/")
def home():
    results = load_results()
    featured = attach_img(online_list(results))[:3]  # 首页精选：前 3 个成果
    total = len(online_list(results))
    views = sum(r.get("views", 0) for r in online_list(results))
    inds = len(set(r["industry"] for r in online_list(results)))
    return render_template("home.html", featured=featured,
                           total=total, views=views, inds=inds, active="home")


@app.route("/works")
def works():
    results = load_results()
    results = attach_img(results)
    tag = request.args.get("tag", "全部")
    tag = tag if tag in TAGS else "全部"
    shown = [r for r in online_list(results) if tag == "全部" or r["tag"] == tag]
    return render_template("works.html", results=shown, tags=TAGS, cur=tag,
                           total=len(online_list(results)), active="works")


@app.route("/work/<int:rid>")
def work(rid):
    results = load_results()
    results = attach_img(results)
    r = next((x for x in results if x["id"] == rid), None)
    if not r:
        abort(404)
    r["views"] = r.get("views", 0) + 1
    save_results(results)
    return render_template("work.html", r=r, active="")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        f = request.form
        title = (f.get("title") or "").strip()
        author = (f.get("author") or "").strip()
        summary = (f.get("summary") or "").strip()
        if not title or not author:
            return render_template("submit.html", tags=TAGS, err="成果名称和创作者必填", active="submit")
        results = load_results()
        results.append({
            "id": next_id(results),
            "title": title,
            "author": author,
            "industry": (f.get("industry") or "").strip() or "其他",
            "tag": f.get("tag") if f.get("tag") in TAGS else "其他",
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
    return render_template("submit.html", tags=TAGS, err="", active="submit")


@app.route("/submit/done")
def submit_done():
    return render_template("submit_done.html", active="")


@app.route("/admin")
def admin():
    results = load_results()
    pending = [r for r in results if r["status"] == "pending"]
    online = online_list(results)
    return render_template("admin.html", pending=pending, online=online, active="")


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
    return render_template("404.html"), 404


if __name__ == "__main__":
    print("Greenthink 启动: http://127.0.0.1:5010")
    app.run(host="0.0.0.0", port=5010, debug=False)
