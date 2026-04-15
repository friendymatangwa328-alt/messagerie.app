from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "secret123"
# Base de données simple
users = {"admin": "1234"}
messages = []
# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/chat")
        else:
            return "Erreur de connexion"
    return render_template("login.html")
# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            return "Utilisateur existe déjà"
        users[username] = password
        return redirect("/")
    return render_template("register.html")
# ================= CHAT =================
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/")
    current_user = session["user"]
    selected_user = request.args.get("user")
    # envoyer message
    if request.method == "POST":
        message = request.form.get("message")
        receiver = request.form.get("receiver")
        if message and receiver:
            messages.append({
                "sender": current_user,
                "receiver": receiver,
                "text": message
            })
    # filtrer messages
    chat_messages = []
    if selected_user:
        for m in messages:
            if (
                (m["sender"] == current_user and m["receiver"] == selected_user)
                or
                (m["sender"] == selected_user and m["receiver"] == current_user)
            ):
                chat_messages.append(m)
    return render_template(
        "chat.html",
        users=users,
        current=current_user,
        selected_user=selected_user,
        messages=chat_messages
    )
# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
