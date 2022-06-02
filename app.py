from flask import Flask, session, redirect, render_template
from flask import request, make_response, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "totes_secret"
debug = DebugToolbarExtension(app)

"""
Survey object
~~~~~~~~~~~~~
survey.title (str)
survey.instructions (str)
survey.questions (Question)

Question object
~~~~~~~~~~~~~~~
question.question (str)
question.choices (list, default is ["Yes", "No"])
question.allow_text (boolean, default is False)
"""

survey = surveys.satisfaction_survey

responses = []

@app.route("/")
def index():
    return render_template("index.html", survey=survey)
    
@app.route("/questions/<q_id>")
def show_question(q_id):
    # Test if user has already filled out survey
    if len(responses) == len(survey.questions):
        return redirect("/thanks")
        
    if not q_id.isnumeric():
        q_id = len(responses)
    elif int(q_id) > len(responses):
        q_id = len(responses)
    else:
        q_id = int(q_id)
    
    return render_template("question.html", question=survey.questions[q_id])

    
@app.route("/answer", methods=["POST"])
def submit_answer():
    if "opt" not in request.form:
        flash("Error: Must select an option")
    
    choice = request.form["opt"]
    responses.append(choice)
    return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")

  
if __name__ == "__main__":
    survey = surveys.satisfaction_survey
    for question in survey.questions:
        print(question.question)