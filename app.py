from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return  render_template("rr.html")

@app.route("/nom/<name>")
def bg(name=None):
    return name+" est un beau gosse"