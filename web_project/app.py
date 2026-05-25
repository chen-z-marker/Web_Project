from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "manjishe_2026"

# MySQL 连接配置
def get_db_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="manjishe",
        charset="utf8mb4"
    )

user_list = {"admin":"123456","user1":"666666"}

@app.route('/')
def index():
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM comic_info")
    comics = cur.fetchall()
    conn.close()
    return render_template("index.html", comics=comics)

@app.route('/category')
def category():
    cate = request.args.get("cate","")
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    if cate:
        cur.execute("SELECT * FROM comic_info WHERE category=%s", (cate,))
    else:
        cur.execute("SELECT * FROM comic_info")
    comics = cur.fetchall()
    conn.close()
    return render_template("category.html", comics=comics)

@app.route('/search', methods=["POST"])
def search():
    key = request.form.get("key","")
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM comic_info WHERE title LIKE %s OR author LIKE %s", (f"%{key}%", f"%{key}%"))
    comics = cur.fetchall()
    conn.close()
    return render_template("search.html", comics=comics)

@app.route('/read/<int:cid>')
def read(cid):
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM comic_info WHERE id=%s", (cid,))
    comic = cur.fetchone()
    conn.close()
    return render_template("read.html", comic=comic)

@app.route('/user')
def user():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("user.html", name=session["username"])

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("pwd")
        if uname in user_list and user_list[uname] == pwd:
            session["username"] = uname
            return redirect("/")
        return "账号密码错误"
    return render_template("login.html")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("pwd")
        if uname in user_list:
            return "账号已存在"
        user_list[uname] = pwd
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)