from flask import Flask, rendre_template
app = Flask(__name__)
@app.route("/")
def home():
    return 
    rendre_template"interface.html"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
