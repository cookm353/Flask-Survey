from flask import Flask, session, redirect, render_template
from flask import request, make_response, DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "totes_secret"
debug = DebugToolbarExtension(app)

responses = []

@app.route("/index")
def index():
    ...
    
@app.route("/questions/<q_num>")
def question():
    ...
    
@app.route("/answer", methods=["POST"])
def answer():
    ...