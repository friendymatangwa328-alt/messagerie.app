from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "secret123"
users = {"admin": "1234"}
messages = []
@app.route("/", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            u = request.form.get("username")
            p = request.form.get("password")
            if u in users and users[u] == p:
                session["user"] = u
                return redirect("/chat")
            return "Erreur connexion"
        return render_template("login.html")
    except Exception as e:
        return str(e)
@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            u = request.form.get("username")
            p = request.form.get("password")
            if u in users:
                return "Utilisateur existe"
            users[u] = p
            return redirect("/")
        return render_template("register.html")
    except Exception as e:
        return str(e)
@app.route("/chat", methods=["GET", "POST"])
def chat():
    try:
        if "user" not in session:
            return redirect("/")
        current = session["user"]
        selected = request.args.get("user")
        if request.method == "POST":
            msg = request.form.get("message")
            receiver = request.form.get("receiver")
            if msg and receiver:
                messages.append({
                    "sender": current,
                    "receiver": receiver,
                    "text": msg
                })
        chat_messages = []
        if selected:
            for m in messages:
                if (
                    (m["sender"] == current and m["receiver"] == selected)
                    or
                    (m["sender"] == selected and m["receiver"] == current)
                ):
                    chat_messages.append(m)
        return render_template("chat.html",
                               users=users,
                               current=current,
                               selected_user=selected,
                               messages=chat_messages)
    except Exception as e:
        return str(e)
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
