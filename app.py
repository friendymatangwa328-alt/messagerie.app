from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder="templates")
# Page login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # ⚠️ Test simple (tu peux changer)
        if username == "admin" and password == "1234":
            return redirect(url_for('interface'))
        else:
            return "Erreur connexion"
    return render_template('login.html')
# Interface principale
@app.route('/interface')
def interface():
    return render_template('interface.html')
# Chat
@app.route('/chat')
def chat():
    return render_template('chat.html')
# Users
@app.route('/users')
def users():
    return render_template('users.html')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
