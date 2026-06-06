from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
import mysql.connector
from flask import send_from_directory
from datetime import datetime

app = Flask(__name__)
app.secret_key = "manjishe_2026"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def get_chapters(cid):
    return [
        {"number": 1, "title": "第1话 初遇", "desc": "故事开始，主角登场"},
        {"number": 2, "title": "第2话 线索", "desc": "新的目标和危机出现"},
        {"number": 3, "title": "第3话 决意", "desc": "进入下一段冒险"},
    ]


def get_chapter_pages(cid, chapter_number, comic):
    chapter_dir = Path(app.root_path) / "static" / "manga" / "chapters" / str(cid) / str(chapter_number)
    if chapter_dir.exists():
        files = sorted(
            item for item in chapter_dir.iterdir()
            if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS
        )
        if files:
            return [
                url_for("static", filename=f"manga/chapters/{cid}/{chapter_number}/{item.name}")
                for item in files
            ]

    return [comic["cover"], comic["cover"], comic["cover"]]

# MySQL连接
def get_db_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="manjishe",
        charset="utf8mb4"
    )

# favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 首页
@app.route('/')
def index():
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM comic_info")
    comics = cur.fetchall()
    conn.close()
    return render_template("index.html", comics=comics)

# 分类
@app.route('/category')
def category():
    cate = request.args.get("cate", "")
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    if cate:
        cur.execute("SELECT * FROM comic_info WHERE category=%s", (cate,))
    else:
        cur.execute("SELECT * FROM comic_info")
    comics = cur.fetchall()
    conn.close()
    return render_template("category.html", comics=comics)

# 搜索
@app.route('/search', methods=["POST"])
def search():
    key = request.form.get("key", "")
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM comic_info WHERE title LIKE %s OR author LIKE %s",
                (f"%{key}%", f"%{key}%"))
    comics = cur.fetchall()
    conn.close()
    return render_template("search.html", comics=comics)

# 收藏/取消收藏
@app.route("/add_fav/<int:cid>")
def add_fav(cid):
    if "username" not in session:
        return redirect("/login")
    un = session["username"]
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM user WHERE username=%s", (un,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return redirect("/login")
    uid = user_row["id"]
    cur.execute("SELECT id FROM favorite WHERE user_id=%s AND comic_id=%s", (uid, cid))
    res = cur.fetchone()
    now = datetime.now()
    if res:
        cur.execute("DELETE FROM favorite WHERE user_id=%s AND comic_id=%s", (uid, cid))
    else:
        cur.execute("INSERT INTO favorite(user_id, comic_id, fav_time) VALUES(%s, %s, %s)",
                    (uid, cid, now))
    conn.commit()
    conn.close()
    return redirect(f"/read/{cid}")

# 加入/移出书架
@app.route("/add_shelf/<int:cid>")
def add_shelf(cid):
    if "username" not in session:
        return redirect("/login")
    un = session["username"]
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM user WHERE username=%s", (un,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return redirect("/login")
    uid = user_row["id"]
    cur.execute("SELECT id FROM bookshelf WHERE user_id=%s AND comic_id=%s", (uid, cid))
    res = cur.fetchone()
    if res:
        cur.execute("DELETE FROM bookshelf WHERE user_id=%s AND comic_id=%s", (uid, cid))
    else:
        cur.execute("INSERT INTO bookshelf(user_id, comic_id, last_chapter) VALUES(%s, %s, %s)",
                    (uid, cid, "最新章节"))
    conn.commit()
    conn.close()
    return redirect(f"/read/{cid}")

# 阅读页（携带收藏、书架状态）
@app.route('/read/<int:cid>')
def read(cid):
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM comic_info WHERE id=%s", (cid,))
    comic = cur.fetchone()
    cur.execute("SELECT * FROM comment WHERE comic_id=%s ORDER BY create_time DESC", (cid,))
    comments = cur.fetchall()

    for c in comments:
        if c['create_time']:
            c['create_time'] = c['create_time'].strftime('%Y-%m-%d %H:%M')

    is_collect = False
    is_shelf = False
    if "username" in session:
        un = session["username"]
        cur.execute("SELECT id FROM user WHERE username=%s", (un,))
        user_row = cur.fetchone()
        if user_row:
            uid = user_row["id"]
            now = datetime.now()
            # 写入阅读记录
            cur.execute("DELETE FROM history WHERE user_id=%s AND comic_id=%s", (uid, cid))
            cur.execute("INSERT INTO history(user_id, comic_id, read_time) VALUES(%s, %s, %s)",
                        (uid, cid, now))
            conn.commit()
            # 判断收藏
            cur.execute("SELECT 1 FROM favorite WHERE user_id=%s AND comic_id=%s", (uid, cid))
            if cur.fetchone():
                is_collect = True
            # 判断书架
            cur.execute("SELECT 1 FROM bookshelf WHERE user_id=%s AND comic_id=%s", (uid, cid))
            if cur.fetchone():
                is_shelf = True

    conn.close()
    is_login = "username" in session
    chapters = get_chapters(cid)
    return render_template("read.html", comic=comic, comments=comments,
                           is_login=is_login, is_collect=is_collect, is_shelf=is_shelf,
                           chapters=chapters)


@app.route('/read/<int:cid>/chapter/<int:chapter_number>')
def chapter(cid, chapter_number):
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM comic_info WHERE id=%s", (cid,))
    comic = cur.fetchone()
    conn.close()

    if not comic:
        abort(404)

    chapters = get_chapters(cid)
    current_chapter = next(
        (item for item in chapters if item["number"] == chapter_number),
        None
    )
    if not current_chapter:
        abort(404)

    pages = get_chapter_pages(cid, chapter_number, comic)
    prev_chapter = next(
        (item for item in chapters if item["number"] == chapter_number - 1),
        None
    )
    next_chapter = next(
        (item for item in chapters if item["number"] == chapter_number + 1),
        None
    )

    return render_template(
        "chapter.html",
        comic=comic,
        chapter=current_chapter,
        pages=pages,
        prev_chapter=prev_chapter,
        next_chapter=next_chapter,
        is_login="username" in session,
    )

# 提交评论
@app.route('/submit_comment/<int:comic_id>', methods=['POST'])
def submit_comment(comic_id):
    if "username" not in session:
        return jsonify({'success': False, 'message': '请先登录账号再评论！'}), 401
    data = request.get_json()
    score = data.get('score')
    content = data.get('content')
    # 从 session 里拿到当前登录的真实用户名
    username = session["username"]

    if not (1 <= score <= 5):
        return jsonify({'success': False, 'message': '评分必须选择1~5星'}), 400
    if not content.strip():
        return jsonify({'success': False, 'message': '评论内容不能为空'}), 400

    conn = get_db_conn()
    cur = conn.cursor()
    try:
        # 确保这里用的是 username 变量
        cur.execute(
            "INSERT INTO comment (comic_id, username, score, content) VALUES (%s, %s, %s, %s)",
            (comic_id, username, score, content)
        )
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        print(e)
        return jsonify({'success': False, 'message': '服务器异常'}), 500
    finally:
        cur.close()
        conn.close()

# 个人中心（已修改SQL，查询带出c.id用于页面跳转）
@app.route('/user')
def user():
    if "username" not in session:
        return redirect("/login")
    un = session["username"]
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM user WHERE username=%s", (un,))
    user_row = cur.fetchone()
    if not user_row:
        session.clear()
        conn.close()
        return redirect("/login")
    uid = user_row["id"]

    # 书架：增加查询 c.id
    cur.execute("""
        SELECT c.id,c.title, c.cover, b.last_chapter FROM bookshelf b
        LEFT JOIN comic_info c ON b.comic_id = c.id WHERE b.user_id=%s
    """, (uid,))
    bookshelf = cur.fetchall()

    # 阅读记录：增加查询 c.id
    cur.execute("""
        SELECT c.id,c.title, c.cover, h.read_time FROM history h
        LEFT JOIN comic_info c ON h.comic_id = c.id WHERE h.user_id=%s
    """, (uid,))
    history = cur.fetchall()

    # 收藏：增加查询 c.id
    cur.execute("""
        SELECT c.id,c.title, c.cover, f.fav_time FROM favorite f
        LEFT JOIN comic_info c ON f.comic_id = c.id WHERE f.user_id=%s
    """, (uid,))
    favorites = cur.fetchall()
    conn.close()

    return render_template('user.html', name=un, bookshelf=bookshelf, history=history, favorites=favorites)

# 登录
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("pwd")
        conn = get_db_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM user WHERE username=%s AND pwd=%s", (uname, pwd))
        row = cur.fetchone()
        conn.close()
        if row:
            session["username"] = uname
            return jsonify({"code":200,"msg":"登录成功"})
        else:
            # 账号密码错误返回弹窗信息
            return jsonify({"code":500,"msg":"账号或密码错误"})
    # GET打开登录页面
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("pwd")
        phone = request.form.get("phone")
        # 手机号格式校验
        if not (len(phone) == 11 and phone.isdigit()):
            return jsonify({"code":500,"msg":"手机号格式不正确"})
        conn = get_db_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO user(username, pwd, phone) VALUES(%s, %s, %s)", (uname, pwd, phone))
            conn.commit()
            conn.close()
            return jsonify({"code":200,"msg":"注册成功"})
        except mysql.connector.IntegrityError:
            conn.close()
            return jsonify({"code":500,"msg":"用户名或手机号已被使用"})
    return render_template("register.html")

# 忘记密码页面+重置密码接口
@app.route('/forget_pwd',methods=["GET","POST"])
def forget_pwd():
    if request.method=="GET":
        return render_template("forget.html")
    # POST重置密码
    phone = request.form.get("phone","").strip()
    new_pwd = request.form.get("new_pwd","").strip()
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    # 查询手机号是否存在
    cur.execute("SELECT id FROM user WHERE phone=%s",(phone,))
    user = cur.fetchone()
    if not user:
        conn.close()
        return jsonify({"code":500,"msg":"该手机号未注册"})
    # 更新密码
    cur.execute("UPDATE user SET pwd=%s WHERE phone=%s",(new_pwd,phone))
    conn.commit()
    conn.close()
    return jsonify({"code":200,"msg":"重置成功"})

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)