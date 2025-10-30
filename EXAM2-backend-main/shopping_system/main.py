from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from datetime import datetime
import sqlite3
import logging
import re 
import os
from pathlib import Path 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-change-me'

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "shopping_data.db"

# 初始logging設定
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# 規則（Email 與密碼至少兩條）
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@gmail\.com$")
HAS_UPPER = re.compile(r"[A-Z]")
HAS_LOWER = re.compile(r"[a-z]")

# 路徑修改
def get_db_connection():
    conn = sqlite3.connect('shopping_data.db')
    if not os.path.exists('shopping_data.db'):
        logging.error(f"Database file not found at {''}")
        return None
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

# 呼叫.html iferror
@app.route('/page_login.html')
def page_login_html_alias():
    return redirect(url_for('page_login'))

@app.route('/page_register.html')
def page_register_html_alias():
    return redirect(url_for('page_register'))

@app.route('/index.html')
def index_html_alias():
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page_register', methods=['GET', 'POST'])
def page_register():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)  # [MOD]
            username = (data.get('username') or '').strip()
            password = (data.get('password') or '').strip()
            email    = (data.get('email') or '').strip()

            # 規則檢查（至少兩條：長度>=8、含大小寫）
            pw_errors = []
            if len(password) < 8:
                pw_errors.append("密碼必須超過8個字元")
            if not HAS_UPPER.search(password) or not HAS_LOWER.search(password):
                pw_errors.append("密碼需包含英文大小寫")

            if pw_errors:
                return jsonify({"status": "error",
                                "message": "、".join(pw_errors) + "，重新輸入"})
            
            if not EMAIL_RE.fullmatch(email):
                return jsonify({"status": "error",
                                "message": "Email 格式不符重新輸入"})
            
            # 寫入/更新 DB
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT username FROM user_table WHERE username = ?", (username,))
            row = cur.fetchone()
            if row:
                # 帳號已存在 -> 覆寫密碼/信箱
                cur.execute("UPDATE user_table SET password=?, email=? WHERE username=?",
                            (password, email, username))
                conn.commit()
                return jsonify({"status": "ok",
                                "message": "帳號已存在，成功修改密碼或信箱"})
            else:
                # 新增
                cur.execute("INSERT INTO user_table(username, password, email) VALUES (?,?,?)",
                            (username, password, email))
                conn.commit()
                return jsonify({"status": "ok",
                                "message": "註冊成功"})
            
        except Exception as e:
            logging.exception("Register error")
            return jsonify({"status": "error", "message": str(e)}), 500

    return render_template('page_register.html')

    return render_template('page_register.html')
def login_user(username, password):
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            user = cursor.fetchone()
            if user:
                return {"status": "success", "message": "登入成功"}
            else:
                return {"status": "error", "message": "帳號或密碼錯誤"}
        except sqlite3.Error as e:
            logging.error(f"Database query error: {e}")
            return {"status": "error", "message": "An error occurred"}
        finally:
            conn.close()
    else:
        return {"status": "error", "message": "Database connection error"}    


@app.route('/page_login' , methods=['GET', 'POST'])
def page_login():
    try:
        if request.method == 'POST':
            data = request.get_json(force=True)  # [MOD] force=True 容忍 header
            username = (data.get('username') or '').strip()
            password = (data.get('password') or '').strip()
            result = login_user(username, password)
            if result["status"] == "success":
                session['username'] = username
            return jsonify(result)
        return render_template('page_login.html')
    except Exception as e:
        logging.exception("Login error")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('page_login'))

# 補齊剩餘副程式
@app.route('/whoami')
def whoami():
    """前端顯示左上角使用者名稱可用此 API"""
    username = session.get('username')
    return jsonify({"username": username or ""})

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'username' not in session:
        return jsonify({"status": "error", "message": "尚未登入"}), 401

    data = request.get_json(force=True)
    items = data.get('items') or []
    if not items:
        return jsonify({"status": "error", "message": "沒有訂單資料"}), 400
    
    username = session['username']
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for it in items:
            name = str(it.get('name') or '')
            price = int(it.get('price') or 0)
            qty = int(it.get('qty') or 0)
            if not name or price <= 0 or qty <= 0:
                continue
            total = price * qty
            cur.execute("""
                INSERT INTO orders(username, Product, Price, Number, Total Price, created_at)
                VALUES (?,?,?,?,?,?)
            """, (username, name, price, qty, total, now_str))
        conn.commit()

    except Exception as e:
        logging.exception("Place order error")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

    return jsonify({"status": "ok", "message": "下單成功"})


# 補齊空缺程式碼
if __name__ == '__main__':
    app.run()


