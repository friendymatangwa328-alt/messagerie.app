from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
# ----- BASE DE DONNÉES -----
def init_db():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
   
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS messages (sender TEXT, receiver TEXT, msg TEXT)")
   
    conn.commit()
    conn.close()
init_db()
# ----- ACCUEIL -----
@app.route("/")
def home():
    return render_template("login.html")
# ----- INSCRIPTION -----
@app.route("/register", methods=["POST"])
def register():
    user = request.form["user"]
    pwd = request.form["pwd"]
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (user,))
    if c.fetchone():
        return "Utilisateur existe déjà"
    c.execute("INSERT INTO users VALUES (?, ?)", (user, pwd))
    conn.commit()
    conn.close()
    return redirect("/")
# ----- CONNEXION -----
@app.route("/login", methods=["POST"])
def login():
    user = request.form["user"]
    pwd = request.form["pwd"]
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
    if c.fetchone():
        return redirect(f"/users/{user}")
    else:
        return "Erreur connexion"
# ----- LISTE DES AMIS -----
@app.route("/users/<user>")
def users_list(user):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    users = [u[0] for u in c.fetchall()]
    conn.close()
    return render_template("users.html", users=users, current=user)
# ----- CHAT (CORRIGÉ) -----
@app.route("/chat/<user1>/<user2>", methods=["GET", "POST"])
def chat(user1, user2):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    if request.method == "POST":
        msg = request.form["msg"]
        if msg != "":
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (user1, user2, msg))
            conn.commit()
    # 🔥 récupère TOUS les messages dans les deux sens
    c.execute("""
        SELECT sender, msg FROM messages
        WHERE (sender=? AND receiver=?)
        OR (sender=? AND receiver=?)
    """, (user1, user2, user2, user1))
    messages = c.fetchall()
    conn.close()
    return render_template("chat.html", messages=messages, user1=user1, user2=user2)
app.run(host="0.0.0.0", port=3000)
