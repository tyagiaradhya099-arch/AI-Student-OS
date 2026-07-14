import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)



from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)

# DATABASE CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"

db = SQLAlchemy(app)


# DATABASE TABLE
class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(200))

    priority = db.Column(db.String(50))

    due_date = db.Column(db.String(50))

    category = db.Column(db.String(50))

    done = db.Column(db.Boolean, default=False)

# NOTES TABLE
class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    content = db.Column(db.Text)

#POMODORO PAGE
class FocusSession(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    minutes = db.Column(db.Integer)

    date = db.Column(db.String(50))


# HOME PAGE
@app.route("/")
def homepage():
    
    tasks = Task.query.all()
    #focus time
    focus_time = db.session.query(
    db.func.sum(FocusSession.minutes)
    ).scalar() or 0
    

    recent_tasks = Task.query.order_by(Task.id.desc()).limit(4).all()

    notes_count = Note.query.count()

    dsa_count = Task.query.filter_by(category="DSA").count()

    web_count = Task.query.filter_by(category="Web Dev").count()

    college_count = Task.query.filter_by(category="College").count()

    personal_count = Task.query.filter_by(category="Personal").count()

    total_tasks = Task.query.count()

    completed_tasks = 0

    for task in tasks:

        if task.done == True:

            completed_tasks += 1

    remaining_tasks = total_tasks - completed_tasks

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f"""
    You are a productivity coach.

    The user has:
    - {remaining_tasks} pending tasks
    - {completed_tasks} completed tasks today
    - {focus_time} minutes of focus today

    Give exactly 3 short productivity tips.

    Rules:
    - maximum 7 words each.
    - No explanations.
    - No numbering.
    - One suggestion per line.
    """
    )
        print(response)
        print("TEXT =",response.text)

        suggestions = response.text.strip().split("\n")

    except Exception as e:
        suggestions = [
            "Complete one pending task today.",
            "Do one Pomodoro session.",
            "Take a 5-minute break after studying."
        ]

      
    return render_template(
        "home.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks,
        dsa_count=dsa_count,
        web_count=web_count,
        college_count=college_count,
        personal_count=personal_count,
        recent_tasks=recent_tasks,
        notes_count=notes_count,
        focus_time=focus_time,
        suggestions=suggestions
        
        
    )


# TASK PAGE
@app.route("/tasks", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # COMPLETE TASK
        if "complete" in request.form:

            task_id = int(request.form["complete"])

            task_to_complete = Task.query.get(task_id)

            if task_to_complete:

                task_to_complete.done = True

                db.session.commit()

        # DELETE TASK
        elif "delete" in request.form:

            task_id = int(request.form["delete"])

            task_to_delete = Task.query.get(task_id)

            if task_to_delete:

                db.session.delete(task_to_delete)

                db.session.commit()

        # CLEAR TASKS
        elif "clear" in request.form:

            Task.query.delete()

            db.session.commit()

        # ADD TASK
        else:

            task = request.form["task"]

            priority = request.form["priority"]

            due_date = request.form["due_date"]

            category = request.form["category"]

            if task.strip() != "":

                new_task = Task(
                  text=task,
                  priority=priority,
                  due_date=due_date,
                  category=category
                )

                db.session.add(new_task)

                db.session.commit()

    # SEARCH TASKS
    search = request.args.get("search")

    if search:

       tasks = Task.query.filter(
         (Task.text.contains(search)) |
         (Task.category.contains(search))
       ).all()

    else:

       tasks = Task.query.all()

    # TASK STATS
    total_tasks = Task.query.count()

    completed_tasks = Task.query.filter_by(done=True).count()

    remaining_tasks = total_tasks - completed_tasks

    if total_tasks == 0:
        progress = 0
    else:
        progress = int((completed_tasks / total_tasks) * 100)

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks,
        progress=progress
    )


# CREATE DATABASE
with app.app_context():

    db.create_all()

    



# NOTES PAGE
@app.route("/notes", methods=["GET", "POST"])
def notes():

    if request.method == "POST":

        if "delete_note" in request.form:

           note_id = request.form["delete_note"]

           note=Note.query.get(note_id)
           
           if note:

             db.session.delete(note)

             db.session.commit()

        else:
           
             title = request.form["title"]

             content = request.form["content"]

             new_note = Note(

              title=title,

              content=content

             )

            
             db.session.add(new_note)

             db.session.commit()

    notes = Note.query.all()


    return render_template(
        "notes.html",
        notes=notes
    )
#POMODORO PAGE
@app.route("/pomodoro")
def pomodoro():

    return render_template("pomodoro.html")

@app.route("/save-focus", methods=["POST"])
def save_focus():

    minutes = request.json["minutes"]

    session = FocusSession(
        minutes=minutes,
        date="2026-07-08"
    )

    db.session.add(session)
    db.session.commit()

    return jsonify({"success": True})

#CALENDER PAGE
@app.route("/calendar")
def calendar():

    tasks = Task.query.order_by(Task.due_date).all()

    return render_template(
        "calendar.html",
        tasks=tasks
    )

#STUDY TRACKER PAGE
@app.route("/study")
def study():

    dsa = Task.query.filter_by(category="DSA").count()

    web = Task.query.filter_by(category="Web Dev").count()

    college = Task.query.filter_by(category="College").count()

    personal = Task.query.filter_by(category="Personal").count()

    total = dsa + web + college + personal

    return render_template(
        "study.html",
        dsa=dsa,
        web=web,
        college=college,
        personal=personal,
        total=total
    )

@app.route("/study-ai", methods=["POST"])
def study_ai():

    prompt = request.form["prompt"]

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f"""
            You are an expert study mentor.

            {prompt}

            Give a practical study plan.
            Keep it under 250 words.
            Use bullet points.
            """
        )

        ai_response = response.text.strip()

    except Exception as e:
        ai_response = f"AI is temporarily unavailable.\n\n{e}"

    dsa = Task.query.filter_by(category="DSA").count()
    web = Task.query.filter_by(category="Web Dev").count()
    college = Task.query.filter_by(category="College").count()
    personal = Task.query.filter_by(category="Personal").count()

    total = dsa + web + college + personal

    return render_template(
        "study.html",
        dsa=dsa,
        web=web,
        college=college,
        personal=personal,
        total=total,
        ai_response=ai_response
    )


#SETTING PAGE
@app.route("/setting")
def setting():
    return render_template("setting.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
