from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# Page d'accueil → login
@app.route('/')
def home():
    return render_template('login.html')
# Page login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # simple vérification (tu peux améliorer après)
        if username == "admin" and password == "1234":
            return redirect(url_for('chat'))
        else:
            return "Erreur connexion"
    return render_template('login.html')
# Page chat
@app.route('/chat')
def chat():
    return render_template('chat.html')
# Page interface
@app.route('/interface')
def interface():
    return render_template('interface.html')
# Page users
@app.route('/users')
def users():
    return render_template('users.html')
# Lancer serveur
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
