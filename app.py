from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "secret123"
users = {"admin": "1234"}
messages = []
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if u in users and users[u] == p:
            session["user"] = u
            return redirect("/chat")
        return "Erreur connexion"
    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if u in users:
            return "Utilisateur existe"
        users[u] = p
        return redirect("/")
    return render_template("register.html")
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/")
    current = session["user"]
    selected = request.args.get("user")
    if request.method == "POST":
        msg = request.form["message"]
        receiver = request.form["receiver"]
        if receiver:
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
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
