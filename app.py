from flask import Flask, session, redirect, render_template
from flask import request, make_response, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "totes_secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
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

# responses = []
# session["responses"] = []

@app.route("/")
def index():
    return render_template("index.html", survey=survey)

@app.route("/start-survey", methods=["POST"])
def start_survey():
    return redirect()
    
@app.route("/questions/<q_id>")
def show_question(q_id):
    responses = session.get("responses", [])
    # Test if user has already filled out survey
    if len(responses) == len(survey.questions):
        return redirect("/thanks")
        
    if not q_id.isnumeric():
        flash("Error: Invalid question number")
        q_id = len(responses)
    elif int(q_id) > len(responses):
        flash("Error: Please answer previous questions first")
        q_id = len(responses)
    elif int(q_id) < len(responses):
        flash("Error: You've already answered that question")
        q_id = len(responses)
    else:
        q_id = int(q_id)
    
    return render_template("question.html", question=survey.questions[q_id])

    
@app.route("/answer", methods=["POST"])
def submit_answer():
    responses = session.get("responses", [])
    if not request.form.get("opt", None):
        flash("Error: Must select an option")
    else:
        choice = request.form["opt"]
        responses.append(choice)
        session['responses'] = responses
        
    print(responses)
    # return redirect(f"/questions/{len(session['responses'])}")
    return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def thanks():
    qa_bundle = zip(session["responses"], survey.questions)
    # return render_template("thanks.html", responses=session['responses'], survey=survey)
    return render_template("thanks.html", qa_bundle=qa_bundle)

  
if __name__ == "__main__":
    survey = surveys.satisfaction_survey
    for question in survey.questions:
        print(question.question)