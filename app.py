from flask import Flask, render_template, request, redirect
app = Flask(__name__)
users = {}
messages = {}
# PAGE ACCUEIL
@app.route("/")
def home():
    return render_template("login.html")
# INSCRIPTION
@app.route("/register", methods=["POST"])
def register():
    user = request.form["user"]
    pwd = request.form["pwd"]
    if user in users:
        return "Utilisateur existe déjà"
   
    users[user] = pwd
    return redirect("/")
# CONNEXION
@app.route("/login", methods=["POST"])
def login():
    user = request.form["user"]
    pwd = request.form["pwd"]
    if user in users and users[user] == pwd:
        return redirect(f"/users/{user}")
    else:
        return "Erreur connexion"
# LISTE DES AMIS
@app.route("/users/<user>")
def liste(user):
    return render_template("users.html", users=users, current=user)
# CHAT
@app.route("/chat/<user1>/<user2>", methods=["GET", "POST"])
def chat(user1, user2):
    key = f"{user1}-{user2}"
    if key not in messages:
        messages[key] = []
    if request.method == "POST":
        msg = request.form["msg"]
        messages[key].append(f"{user1}: {msg}")
    return render_template("chat.html", messages=messages[key], user1=user1, user2=user2)
app.run(host="0.0.0.0", port=3000)
