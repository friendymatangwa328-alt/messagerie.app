from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "secret123"
# Stockage temporaire (mémoire)
users = {
    "admin": "1234"
}
messages = []  # Liste des messages
# PAGE LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/chat")
        return "Erreur connexion"
    return render_template("login.html")
# PAGE REGISTER
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
# PAGE CHAT
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/")
    current_user = session["user"]
    selected_user = request.args.get("user")
    # envoyer message
    if request.method == "POST":
        msg = request.form["message"]
        receiver = request.form["receiver"]
        messages.append({
            "sender": current_user,
            "receiver": receiver,
            "text": msg
        })
    # filtrer messages entre 2 personnes
    filtered_messages = []
    if selected_user:
        for m in messages:
            if (
                (m["sender"] == current_user and m["receiver"] == selected_user)
                or
                (m["sender"] == selected_user and m["receiver"] == current_user)
            ):
                filtered_messages.append(m)
    return render_template(
        "chat.html",
        users=users,
        current=current_user,
        selected_user=selected_user,
        messages=filtered_messages
    )
# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
# LANCEMENT
if __name__ == "__main__":
    app.run(debug=True)
