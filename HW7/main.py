from flask import Flask, render_template, request, redirect, url_for, g, session, flash
import sqlite3, os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-change-me'
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("login method =", request.method) 

        uname = (request.form.get("username") or "").strip()
        pwd   = (request.form.get("password") or "").strip()

        # 先查「名稱是否存在」
        con = get_db()
        row = con.execute("SELECT username, password FROM teachers WHERE username=?",
                          (uname,)).fetchone()
        con.close()

        if row is None:
            print("return: name error") 
            # 名稱錯誤（完全查不到這個 username）
            flash("錯誤的名稱", "error")
            return render_template("login.html", username=uname)

        if pwd != row["password"]:
            print("return: pwd error")
            # 名稱存在，但密碼對不起來
            flash("錯誤的密碼", "error")
            return render_template("login.html", username=uname)

        # 成功：寫入 session，導到下一頁（先放 placeholder）
        session["teacher_name"] = row["username"]
        flash("登入成功", "ok")
        print("return: success -> redirect /grades")
        return redirect(url_for("grades"))  # 之後做成績頁
    # GET 需要回傳畫面
    print("return: GET login page") 
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("你已登出", "ok")
    return redirect(url_for("login"))


@app.route("/grades", methods=["GET", "POST"])
def grades():
    # 必須登入
    name = session.get("teacher_name")
    if not name:
        return redirect(url_for("login"))

    if request.method == "POST":
        action = request.form.get("action")

        con = get_db()
        try:
            if action == "add":
                name = (request.form.get("name") or "").strip()
                student_id   = (request.form.get("student_id") or "").strip()
                score_raw    = (request.form.get("score") or "").strip()

                if not name or not student_id or not score_raw.isdigit():
                    flash("輸入不完整或成績不是數字", "error")
                else:
                    score = int(score_raw)
                    try:
                        con.execute(
                            "INSERT INTO grades(name, student_id, score) VALUES (?,?,?)",
                            (name, student_id, score)
                        )
                        con.commit()
                        flash("已新增", "ok")
                    except sqlite3.IntegrityError:
                        # student_id UNIQUE → 改為更新
                        con.execute(
                            "UPDATE grades SET name=?, score=? WHERE student_id=?",
                            (name, score, student_id)
                        )
                        con.commit()
                        flash("學號已存在，已改為更新", "ok")

            elif action == "delete":
                sid = (request.form.get("delete_student_id") or "").strip()
                if sid:
                    con.execute("DELETE FROM grades WHERE student_id=?", (sid,))
                    con.commit()
                    flash("已刪除（若該學號存在）", "ok")
        finally:
            con.close()

        return redirect(url_for("grades"))  # PRG 模式，避免重送表單

    # GET：查表格（學號小到大）
    con = get_db()
    try:
        rows = con.execute(
            "SELECT name, student_id, score FROM grades ORDER BY CAST(student_id AS INTEGER)"
        ).fetchall()
    finally:
        con.close()

    return render_template("grades.html", rows=rows)