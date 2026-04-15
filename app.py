from flask import Flask, render_template, request, redirect, session
import sqlite3
app = Flask(__name__)
app.secret_key = "secret123"
# ----- DATABASE -----
def init_db():
    conn = sqlite3.connect("db.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS messages (username TEXT, message TEXT)")
    conn.commit()
    conn.close()
init_db()
# ----- ACCUEIL -----
@app.route('/')
def home():
    return redirect('/login')
# ----- INSCRIPTION -----
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect("db.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        return "Utilisateur existe déjà"
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return redirect('/login')
# ----- LOGIN -----
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect("db.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect('/chat')
        else:
            return "Erreur connexion"
    return render_template('login.html')
# ----- CHAT -----
@app.route('/chat')
def chat():
    conn = sqlite3.connect("db.db")
    c = conn.cursor()
    c.execute("SELECT * FROM messages")
    messages = c.fetchall()
    c.execute("SELECT username FROM users")
    users = c.fetchall()
    conn.close()
    return render_template("chat.html",
                           messages=messages,
                           users=users,
                           username=session.get('username'))
# ----- ENVOI MESSAGE -----
@app.route('/send', methods=['POST'])
def send():
    message = request.form.get('message')
    username = session.get('username')
    conn = sqlite3.connect("db.db")
    c = conn.cursor()
    if message:
        c.execute("INSERT INTO messages VALUES (?, ?)", (username, message))
        conn.commit()
    conn.close()
    return redirect('/chat')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
