from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def survey_page():
    """Survey base page"""
    return render_template("survey_page.html", survey=satisfaction_survey)

@app.route("/start", methods=["POST"])
def start_vars():
    """Initialize the responses list as a session cookie"""
    session['responses'] = []
    return redirect("/questions/0")

# @app.route("/questions", methods=["POST"])
# def questions_page():
#     """Start questions"""
#    return redirect("/questions/0")

@app.route("/questions/<int:id>")
def question(id):
    """Show actual question based on ID.
    This uses <int:x> to specify it is an int"""
    responses = session.get('responses')
    print(responses)

    if(responses is None):
        return redirect("/")

    if(len(responses) != id):
        flash("YOU NEED TO ANSWER THIS QUESTION FIRST!")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[id]

    return render_template("q.html", qNum = id, question=question)

@app.route("/user_info", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    choice = request.form['info']

    """Appending list in session, need to rebind"""
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    if (len(responses) == len(satisfaction_survey.questions)):        
        return redirect("/done")

    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/done")
def done():
    """Thank person for finishing the survey and show what they said"""

    return render_template("done.html", data=session['responses'])    