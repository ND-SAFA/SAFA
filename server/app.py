from flask import Flask, app

app = Flask(__name__)

@app.route("/")
def root():
    return "Hello World"