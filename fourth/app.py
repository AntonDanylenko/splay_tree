from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def landing():
    return "static/landing.html"
