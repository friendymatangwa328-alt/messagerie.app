from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# Page d'accueil → redirige vers login
@app.route('/')
def home():
    return redirect('/login')
# Page login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/chat')
    return render_template('login.html')
# Page chat
@app.route('/chat')
def chat():
    return render_template('chat.html')
# Page interface
@app.route('/interface')
def interface():
    return render_template('interface.html')
# Page utilisateurs
@app.route('/users')
def users():
    return render_template('users.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
