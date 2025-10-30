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
   
@app.route('/page_register', methods=[])
def page_register():
    if request.method == 'POST':
        data = request.get_json()
       # 補齊空缺程式碼
        if ...
            return jsonify({"status": "error", "message": "此名稱已被使用"})

        if len(password) < 8:
       ...
       

    return render_template('page_register.html')


def login_user(username, password):
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                return {"status": "success", "message": "Login successful"}
            else:
                return {"status": "error", "message": "Invalid username or password"}
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
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            result = login_user(username, password)
            if result["status"] == "success":
                session['username'] = username
            return jsonify(result)
        return render_template('page_login.html')
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 補齊剩餘副程式


# 補齊空缺程式碼
if __name__ == '__main__':
    app.run()


