# -*- coding: utf-8 -*-
"""Greenthink —— 你的创意，应该被看见
Flask + JSON 存储：官网首页 / 成果展厅 / 作品详情 / 提交 / 管理（审核）
中英双语（i18n）· 管理员登录保护 · 图片/视频上传 · 端口 5010
"""
import html as html_lib
import json
import os
import re
import threading
import uuid
import zipfile
from datetime import date
from xml.etree import ElementTree as ET

from flask import (Flask, abort, redirect, render_template, request, session,
                   url_for)
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "results.json")
IMG_DIR = os.path.join(BASE_DIR, "static", "img", "works")
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")
LOCK = threading.Lock()

# ═══ 管理员密码：从环境变量读取，未设置时用默认值（仅本地开发用）═══
# Windows 设置（新开终端生效）：
#   setx GREENTHINK_ADMIN_PASSWORD "你的强密码"
ADMIN_PASSWORD = os.environ.get("GREENTHINK_ADMIN_PASSWORD") or "greenthink2026"

app = Flask(__name__)
app.secret_key = "greenthink-creative-showcase"
app.json.sort_keys = False
app.config["MAX_CONTENT_LENGTH"] = 60 * 1024 * 1024  # 上传上限 60MB

# 上传白名单
ALLOWED_IMAGES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
ALLOWED_VIDEOS = {".mp4", ".webm", ".mov"}
ALLOWED_DOCS = {".pdf", ".doc", ".docx"}
ALLOWED_ALL = ALLOWED_IMAGES | ALLOWED_VIDEOS | ALLOWED_DOCS

os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        "work_story": "作品故事",
        "work_problem": "遇到的问题", "work_solution": "创意的解法", "work_result": "最终结果",
        "work_cta": "你也做出了成果？提交你的作品，让更多人看见。",
        "submit_title": "提交你的创意成果",
        "submit_sub": "3 分钟搞定：填名称、简介、署名，配一张图，你的成果就能被看见。",
        "form_title": "成果名称", "form_author": "创作者署名",
        "form_tag": "分类", "form_summary": "一句话简介",
        "form_story": "作品故事（选填）",
        "form_story_hint": "它解决了什么问题？你怎么用AI做出来的？最终效果如何？一段话讲完就行",
        "form_link": "体验链接（选填）",
        "form_images": "作品图片（可多张，第一张作封面，支持 jpg/png/webp/gif）",
        "form_video": "作品视频（选填，建议 H.264 编码的 mp4；手机默认 HEVC 编码可能无法播放）",
        "form_doc": "作品文档（选填，PDF/Word，放完整方案、图集或说明）",
        "video_hint": "视频无法播放？多为浏览器不支持 HEVC 编码（手机拍摄常见），可下载后播放",
        "video_download": "下载视频",
        "doc_open": "新窗口打开", "doc_download": "下载文档",
        "tab_images": "图片", "tab_video": "视频", "tab_doc": "文档",
        "form_optional": "选填",
        "submit_btn": "提交成果", "browse_btn": "先逛逛展厅",
        "submit_ok": "✅ 提交成功", "submit_ok_sub": "你的创意成果已进入审核队列，通过后会展示在展厅里。",
        "ph_title": "如：山海方言录", "ph_summary": "它是做什么的？一句话说清",
        "ph_author": "你的名字或昵称",
        "ph_story": "它解决了什么问题？\n你怎么用AI做出来的？\n最终效果如何？",
        "admin_title": "成果管理", "admin_pending": "⏳ 待审核", "admin_online": "🟢 已上线",
        "admin_preview": "预览", "admin_approve": "通过", "admin_delete": "删除",
        "admin_login": "管理员登录", "admin_pass": "密码", "admin_login_btn": "登录",
        "admin_logout": "退出登录", "admin_wrong": "密码错误，请重试",
        "admin_denied": "请先登录管理员账号",
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
        "work_story": "The Story",
        "work_problem": "The Problem", "work_solution": "The Creative Solution", "work_result": "The Final Result",
        "work_cta": "Made something too? Submit your work and let it be seen.",
        "submit_title": "Submit Your Creation",
        "submit_sub": "Done in 3 minutes: title, summary, your name, one image — and your work gets seen.",
        "form_title": "Work Title", "form_author": "Creator Name",
        "form_tag": "Category", "form_summary": "One-line Summary",
        "form_story": "The story (optional)",
        "form_story_hint": "What problem does it solve? How did you make it with AI? What's the result?",
        "form_link": "Experience link (optional)",
        "form_images": "Work images (multiple OK, first is cover; jpg/png/webp/gif)",
        "form_video": "Work video (optional; H.264 mp4 recommended — phone HEVC may not play in browsers)",
        "form_doc": "Work document (optional; PDF/Word — full plan, album or description)",
        "video_hint": "Video not playing? Likely HEVC (H.265) from phones — browsers may not support it. Download to watch.",
        "video_download": "Download video",
        "doc_open": "Open", "doc_download": "Download",
        "tab_images": "Images", "tab_video": "Video", "tab_doc": "Document",
        "form_optional": "Optional",
        "submit_btn": "Submit Work", "browse_btn": "Browse Gallery",
        "submit_ok": "✅ Submitted", "submit_ok_sub": "Your creation is in the review queue and will appear in the gallery once approved.",
        "ph_title": "e.g. A Dialect Bestiary", "ph_summary": "What is it? One sentence",
        "ph_author": "Your name or nickname",
        "ph_story": "What problem does it solve?\nHow did you make it with AI?\nWhat is the result?",
        "admin_title": "Manage Creations", "admin_pending": "⏳ Pending Review", "admin_online": "🟢 Live",
        "admin_preview": "Preview", "admin_approve": "Approve", "admin_delete": "Delete",
        "admin_login": "Admin Login", "admin_pass": "Password", "admin_login_btn": "Log in",
        "admin_logout": "Log out", "admin_wrong": "Wrong password, try again",
        "admin_denied": "Please log in as admin first",
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


# ═══════════ 工具函数 ═══════════

def load_results():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["results"]


def save_results(results):
    with LOCK:
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"results": [
                {k: v for k, v in r.items() if k != "has_img"}  # 剥离临时计算字段
                for r in results
            ]}, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DATA_FILE)


def next_id(results):
    return max((r["id"] for r in results), default=0) + 1


def online_list(results):
    return [r for r in results if r["status"] == "online"]


def attach_img(results):
    """成果 id 对应 static/img/works/<id>.jpg 存在则标记 has_img（兼容旧的 id 配图）"""
    for r in results:
        r["has_img"] = any(
            os.path.exists(os.path.join(IMG_DIR, f"{r['id']}{ext}"))
            for ext in IMG_EXTS
        )
        r.setdefault("images", [])
        r.setdefault("video", "")
        r.setdefault("story", "")
        r.setdefault("doc", "")
        r.setdefault("doc_name", "")
    return results


def cover_of(r):
    """卡片封面优先级：上传图第一张 > id 配图 > 渐变占位"""
    if r.get("images"):
        return r["images"][0]
    if r.get("has_img"):
        return url_for("static", filename=f"img/works/{r['id']}.jpg")
    return ""


def save_upload(file_storage):
    """保存上传文件，返回 /static/uploads/xxx 相对路径；非法返回 None"""
    if not file_storage or not file_storage.filename:
        return None
    ext = os.path.splitext(file_storage.filename)[1].lower()
    if ext not in ALLOWED_ALL:
        return None
    name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, name)
    file_storage.save(path)
    if not sniff_ok(path, ext):
        try:
            os.remove(path)
        except OSError:
            pass
        return None
    return f"/static/uploads/{name}"


def sniff_ok(path, ext):
    """校验文件内容与扩展名是否名副其实（防假文件）"""
    try:
        with open(path, "rb") as f:
            head = f.read(12)
    except OSError:
        return False
    if ext == ".pdf":
        return head.startswith(b"%PDF-")
    if ext in (".jpg", ".jpeg"):
        return head.startswith(b"\xff\xd8\xff")
    if ext == ".png":
        return head.startswith(b"\x89PNG")
    if ext == ".webp":
        return head[:4] == b"RIFF" and head[8:12] == b"WEBP"
    if ext == ".gif":
        return head.startswith(b"GIF8")
    if ext in (".mp4", ".mov"):
        return head[4:8] == b"ftyp"
    if ext == ".webm":
        return head.startswith(b"\x1aE\xdf\xa3")
    if ext == ".docx":
        return head.startswith(b"PK\x03\x04")
    if ext == ".doc":
        return head.startswith(b"\xd0\xcf\x11\xe0")
    return True


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def docx_to_html(path):
    """用标准库把 docx 解析为简单 HTML（段落+表格），失败返回 None"""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        root = ET.fromstring(xml)
        body = root.find(W + "body")
        if body is None:
            return None
        out = []
        for child in body:
            if child.tag == W + "p":
                text = "".join(t.text or "" for t in child.iter(W + "t"))
                text = text.replace("\t", "　")
                out.append(f"<p>{html_lib.escape(text) or '&nbsp;'}</p>")
            elif child.tag == W + "tbl":
                rows = []
                for tr in child.findall(W + "tr"):
                    cells = []
                    for tc in tr.findall(W + "tc"):
                        ctext = "".join(t.text or "" for t in tc.iter(W + "t")).strip()
                        cells.append(f"<td>{html_lib.escape(ctext)}</td>")
                    rows.append("<tr>" + "".join(cells) + "</tr>")
                out.append("<table>" + "".join(rows) + "</table>")
        return "".join(out)
    except Exception:
        return None


def lang_of():
    return session.get("lang", "zh") if session.get("lang") in UI else "zh"


def ctx(**kw):
    lang = lang_of()
    kw["lang"] = lang
    kw["T"] = UI[lang]
    kw["is_admin"] = is_admin()
    return kw


def is_admin():
    return session.get("admin") is True


def admin_required(view):
    from functools import wraps

    @wraps(view)
    def wrapper(*a, **kw):
        if not is_admin():
            return redirect(url_for("admin_login", next=request.path))
        return view(*a, **kw)

    return wrapper


# ═══════════ 语言切换 ═══════════

@app.route("/lang/<code>")
def set_lang(code):
    if code in UI:
        session["lang"] = code
    return redirect(request.referrer or url_for("home"))


# ═══════════ 公开页面 ═══════════

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
    r["docx_html"] = ""
    if r.get("doc") and r["doc"].lower().endswith(".docx"):
        r["docx_html"] = docx_to_html(
            os.path.join(BASE_DIR, r["doc"].lstrip("/"))) or ""
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
            return render_template("submit.html", tags=TAGS,
                                   err="成果名称和创作者必填 / Title and creator are required",
                                   active="submit", **ctx())

        # 保存上传的图片与视频
        images = []
        for img in request.files.getlist("images"):
            path = save_upload(img)
            if path and path.lower().endswith(tuple(ALLOWED_IMAGES)):
                images.append(path)
        video = ""
        vf = request.files.get("video")
        if vf and vf.filename:
            vpath = save_upload(vf)
            if vpath and vpath.lower().endswith(tuple(ALLOWED_VIDEOS)):
                video = vpath
        doc = ""
        doc_name = ""
        df = request.files.get("doc")
        if df and df.filename:
            dpath = save_upload(df)
            if dpath and dpath.lower().endswith(tuple(ALLOWED_DOCS)):
                doc = dpath
                doc_name = df.filename[:60]
            else:
                return render_template(
                    "submit.html", tags=TAGS,
                    err="文档不是有效的 PDF/Word 文件（可能是网页另存为的假文件），请上传真正的文件",
                    active="submit", **ctx())

        results = load_results()
        results.append({
            "id": next_id(results),
            "title": title,
            "author": author,
            "industry": (f.get("industry") or "").strip() or "Other",
            "tag": f.get("tag") if f.get("tag") in TAG_VALUES else "其他",
            "summary": summary,
            "story": (f.get("story") or "").strip(),
            "problem": (f.get("problem") or "").strip(),
            "solution": (f.get("solution") or "").strip(),
            "result": (f.get("result") or "").strip(),
            "effects": [x.strip() for x in (f.get("effects") or "").splitlines() if x.strip()],
            "link": (f.get("link") or "").strip(),
            "images": images,
            "video": video,
            "doc": doc,
            "doc_name": doc_name,
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


# ═══════════ 管理后台（登录保护） ═══════════

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if (request.form.get("password") or "") == ADMIN_PASSWORD:
            session["admin"] = True
            nxt = request.args.get("next")
            return redirect(nxt if nxt and nxt.startswith("/") else url_for("admin"))
        return render_template("admin_login.html", err=UI[lang_of()]["admin_wrong"], **ctx())
    return render_template("admin_login.html", err="", **ctx())


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


@app.route("/admin")
@admin_required
def admin():
    results = load_results()
    pending = [r for r in results if r["status"] == "pending"]
    online = online_list(results)
    return render_template("admin.html", pending=pending, online=online, active="", **ctx())


@app.route("/admin/approve/<int:rid>", methods=["POST"])
@admin_required
def approve(rid):
    results = load_results()
    for r in results:
        if r["id"] == rid:
            r["status"] = "online"
            break
    save_results(results)
    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:rid>", methods=["POST"])
@admin_required
def delete(rid):
    results = load_results()
    target = next((r for r in results if r["id"] == rid), None)
    results = [r for r in results if r["id"] != rid]
    save_results(results)
    if target:
        for img in target.get("images", []):
            try:
                os.remove(os.path.join(BASE_DIR, img.lstrip("/")))
            except OSError:
                pass
        if target.get("video"):
            try:
                os.remove(os.path.join(BASE_DIR, target["video"].lstrip("/")))
            except OSError:
                pass
        if target.get("doc"):
            try:
                os.remove(os.path.join(BASE_DIR, target["doc"].lstrip("/")))
            except OSError:
                pass
    return redirect(url_for("admin"))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", **ctx()), 404


if __name__ == "__main__":
    print("Greenthink 启动: http://127.0.0.1:5010")
    print(f"管理员登录: http://127.0.0.1:5010/admin/login （密码: {ADMIN_PASSWORD}，请在 app.py 顶部修改）")
    app.run(host="0.0.0.0", port=5010, debug=False)
