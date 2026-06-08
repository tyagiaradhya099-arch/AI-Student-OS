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

    done = db.Column(db.Boolean, default=False)


# HOME PAGE
@app.route("/")
def homepage():

    return render_template("home.html")


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

            if task.strip() != "":

                new_task = Task(
                    text=task,
                    priority=priority
                )

                db.session.add(new_task)

                db.session.commit()

    # FETCH ALL TASKS
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


if __name__ == "__main__":
    app.run(debug=True)