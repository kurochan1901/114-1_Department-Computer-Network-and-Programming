import re, sqlite3, os
from getpass import getpass

DB_path = "HW6/users.db"

Email_RE = re.compile(r"^[A-Za-z0-9._%+-]+@gmail\.com$")
Special_RE = re.compile(r"[^\w]")
Upper_RE   = re.compile(r"[A-Z]")
Lower_RE   = re.compile(r"[a-z]")

def connect_db():
    if not os.path.exists(DB_path):
        print(f"[!] can't find {DB_path}")
    return sqlite3.connect(DB_path)

def table_check(cur) -> bool:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_data'")
    if cur.fetchone() is None:
        print("[!] can't find user_data")
        return False
    return True

def check_password_rules(pwd: str):
    errs = []
    if len(pwd) < 8:
        errs.append("The password must be at least 8 characters long")
    if not Upper_RE.search(pwd) or not Lower_RE.search(pwd):
        errs.append("The password must contain both uppercase and lowercase letters")
    if not Special_RE.search(pwd):
        errs.append("The password must contain at least one special character (!@#$%^&*()_+.)")
    return errs

def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s: return s
        print("Input cannot be empty, please try again.")

# sign up
def sign_up(conn: sqlite3.Connection):
    print("\n== sign up ==")
    name = input_nonempty("Name: ")

    # Email
    while True:
        email = input_nonempty("Email: ")
        if Email_RE.fullmatch(email):
            break
        print("The email format is invalid (XXX@gmail.com). Please enter again.")

    # Password
    cancel_token = "!q"
    while True:

        pwd = getpass(f"Password (or enter {cancel_token} to cancel): ")
        if pwd == cancel_token:
            print("Cancelled sign up. Back to the home page.")
            return

        errs = check_password_rules(pwd)
        if errs:
            print("The password is invalid: " + "、".join(errs))
        else:
            pwd2 = getpass("Password again(or enter {cancel_token} to cancel): ")
            if pwd2 == cancel_token:
                print("Cancelled sign up. Back to the home page.")
                return
            if pwd == pwd2:
                break
            else:
                print("Passwords do not match. Please enter again.")

    # preview and confirm
    print(f"save {name} | {email} | {pwd} | Y / N ? (Y: update/save, N: cancel)")
    if input("-> ").strip().lower() != "y":
        print("Cancelled sign up. Back to the home page.")
        return

    # insert data into user_table
    cur = conn.cursor()
    cur.execute("SELECT rowid FROM user_data WHERE email = ?", (email,))
    row = cur.fetchone()

    if row is None:
        cur.execute("INSERT INTO user_data(name, email, password) VALUES (?, ?, ?)",
                    (name, email, pwd))
        conn.commit()
        print("New user added.")
    else:
        print("Email already exists. Update information? (Y: update/ N: re-enter email)")
        if input("-> ").strip().lower() == "y":
            cur.execute("UPDATE user_data SET name=?, password=? WHERE email=?",
                        (name, pwd, email))
            conn.commit()
            print("User information updated.")
        else:
            print("Cancelled update.")

# sign in
def sign_in(conn: sqlite3.Connection):
    print("\n== sign in ==")
    name  = input_nonempty("Name: ")
    email = input_nonempty("Email: ")

    cur = conn.cursor()
    cur.execute("SELECT password FROM user_data WHERE name=? AND email=?", (name, email))
    row = cur.fetchone()
    if row is None:
        print("Name or email not found.(press a to sign up/ press any key to return)")
        if input("-> ").strip().lower() == "a":
            sign_up(conn)
        return

    # password check
    while True:
        pwd = getpass("Password: ")
        if pwd != row[0]:
            print("Password incorrect.Forget password? (Y / N )")
            if input("-> ").strip().lower() == "y":
                print("Switch to sign up page (allowing password update or reset)")
                sign_up(conn)
                return
        else:
            print("Sign in successful. Welcome back!")
            return

def main():
    print("=== HW6-2 sign up/ sign in system ===")
    conn = connect_db()
    with conn:
        cur = conn.cursor()
        if not table_check(cur):
            return
    try:
        while True:
            print("\n== enter system ==")
            print("(a) sign up  |  (b) sign in  |  (q) quit")
            choice = input("choose: ").strip().lower()
            if choice == "a":
                sign_up(conn)
            elif choice == "b":
                sign_in(conn)
            elif choice == "q":
                print("Bye."); break
            else:
                print("Invalid input, please try again.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
