from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

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


# HOME PAGE
@app.route("/")
def homepage():
    
    tasks = Task.query.all()

    dsa_count = Task.query.filter_by(category="DSA").count()

    web_count = Task.query.filter_by(category="Web Dev").count()

    college_count = Task.query.filter_by(category="College").count()

    personal_count = Task.query.filter_by(category="Personal").count()

    total_tasks = len(tasks)

    completed_tasks = 0

    for task in tasks:

        if task.done == True:

            completed_tasks += 1

    remaining_tasks = total_tasks - completed_tasks

    return render_template(
        "home.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks,
        dsa_count=dsa_count,
        web_count=web_count,
        college_count=college_count,
        personal_count=personal_count
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
    total_tasks = len(tasks)

    completed_tasks = 0

    for task in tasks:

        if task.done == True:

            completed_tasks += 1

    remaining_tasks = total_tasks - completed_tasks

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks
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


if __name__ == "__main__":


    app.run(debug=True)

