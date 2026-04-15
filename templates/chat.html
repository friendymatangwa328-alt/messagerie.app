from flask import Flask, render_template, request, redirect
app = Flask(__name__)
# Stockage temporaire des messages
messages = []
# Page accueil → login
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
    return render_template('chat.html', messages=messages)
# Envoi message
@app.route('/send', methods=['POST'])
def send():
    message = request.form.get('message')
    if message:
        messages.append(message)
    return redirect('/chat')
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
