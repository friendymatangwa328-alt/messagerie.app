from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "secret123"
# Base simple (mémoire)
users = {
    "admin": "1234"
}
messages = []  # {sender, receiver, text}
# 🔐 LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect("/chat")
        else:
            return "Erreur connexion"
    return render_template("login.html")
# 📝 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            return "Utilisateur existe déjà"
        users[username] = password
        return redirect("/")
    return render_template("register.html")
# 💬 CHAT PRIVÉ
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect("/")
    sender = session["username"]
    receiver = request.args.get("user")
    if request.method == "POST":
        msg = request.form["message"]
        if receiver:
            messages.append({
                "sender": sender,
                "receiver": receiver,
                "text": msg
            })
    # Filtrer messages
    filtered = []
    if receiver:
        for m in messages:
            if (m["sender"] == sender and m["receiver"] == receiver) or \
               (m["sender"] == receiver and m["receiver"] == sender):
                filtered.append(m)
    return render_template(
        "chat.html",
        users=users,
        current=sender,
        receiver=receiver,
        messages=filtered
    )
# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
