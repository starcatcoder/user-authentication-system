from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
import sqlite3
from datetime import timedelta
from time import time

# =========================
# APP CONFIG
# =========================
app = Flask(__name__)
app.secret_key = "chave_secreta_simples"

app.permanent_session_lifetime = timedelta(minutes=30)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_REFRESH_EACH_REQUEST=True
)

bcrypt = Bcrypt(app)
DATABASE = "database.db"
# =========================
# SESSION TIMER PARA O FRONTEND
# =========================
login_attempts = {}

@app.context_processor
def inject_session_timer():
    if "user" in session:
        remaining = int(app.permanent_session_lifetime.total_seconds())
        return dict(session_time=remaining)
    return dict(session_time=0)

# =========================
# FUNÇÃO AUXILIAR DB
# =========================
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    ip = request.remote_addr
    now = time()

    # Proteção contra força bruta
    if ip in login_attempts:
        attempts, last_time = login_attempts[ip]
        if attempts >= 5 and now - last_time < 300:
            flash("Muitas tentativas. Tente novamente em alguns minutos.", "error")
            return render_template("login.html")

        if now - last_time >= 300:
            login_attempts[ip] = (0, now)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        success = 1 if user and bcrypt.check_password_hash(user["password"], password) else 0

        # 🔐 Registrar tentativa de login
        cursor.execute(
            "INSERT INTO login_logs (username, ip, success) VALUES (?, ?, ?)",
            (username, ip, success)
        )
        conn.commit()
        conn.close()

        if success:
            session["user"] = user["username"]
            session["theme"] = user["theme"]
            session["login_success"] = True
            session.permanent = True
            login_attempts.pop(ip, None)
            return redirect("/dashboard")
        else:
            attempts, _ = login_attempts.get(ip, (0, now))
            login_attempts[ip] = (attempts + 1, now)
            flash("Usuário ou senha inválidos", "error")

    return render_template("login.html")


# =========================
# CADASTRO
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password, theme) VALUES (?, ?, ?)",
                (username, hashed, "light")
            )
            conn.commit()
            flash("Cadastro realizado com sucesso!", "success")
            return redirect("/")
        except sqlite3.IntegrityError:
            flash("Usuário já existe", "error")
        finally:
            conn.close()

    return render_template("register.html", theme=session.get("theme", "light"))

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    conn.close()

    theme = session.get("theme", "light")
    login_success = session.pop("login_success", None)

    return render_template(
        "dashboard.html",
        user=session["user"],
        total_users=total_users,
        theme=theme,
        login_success=login_success
    )

# =========================
# SALVAR TEMA
# =========================
@app.route("/theme", methods=["POST"])
def change_theme():
    if "user" not in session:
        return "", 204

    data = request.get_json()
    theme = data.get("theme", "light")

    session["theme"] = theme

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET theme = ? WHERE username = ?",
        (theme, session["user"])
    )
    conn.commit()
    conn.close()

    return "", 204


@app.route("/logs")
def logs():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_logs ORDER BY timestamp DESC LIMIT 20")
    logs = cursor.fetchall()
    conn.close()

    return render_template("logs.html", logs=logs)

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def create_logs_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            ip TEXT,
            success INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    create_logs_table()
    print("🚀 Servidor Flask iniciando...")
    app.run(debug=True)


