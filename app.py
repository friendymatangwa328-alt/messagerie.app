from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder="templates")
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "1234":
            return redirect(url_for('interface'))
        else:
            return "Erreur connexion"
    return render_template('login.html')
@app.route('/interface')
def interface():
    return render_template('interface.html')
@app.route('/chat')
def chat():
    return render_template('chat.html')
@app.route('/users')
def users():
    return render_template('users.html')
app.run(host="0.0.0.0", port=3000)
