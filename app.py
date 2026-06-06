from flask import Flask, render_template, request

app = Flask(__name__)

tasks = []

#HOME PAGE
@app.route("/")
def homepage():

    return render_template("home.html")

#TASK PAGE 
@app.route("/tasks", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # COMPLETE TASK
        if "complete" in request.form:

            index = int(request.form["complete"])

            if 0 <= index < len(tasks):

                tasks[index]["done"] = True

        # DELETE TASK
        elif "delete" in request.form:

            index = int(request.form["delete"])

            if 0 <= index < len(tasks):

                tasks.pop(index)

        # CLEAR TASKS
        elif "clear" in request.form:

            tasks.clear()

        # ADD TASK
        else:

            task = request.form["task"]

            priority = request.form["priority"]

            if task.strip() != "":

                tasks.append({
                    "text": task,
                    "done": False,
                    "priority": priority
                })

    # TASK STATS
    total_tasks = len(tasks)

    completed_tasks = 0

    for task in tasks:

        if task["done"] == True:

            completed_tasks += 1

    remaining_tasks = total_tasks - completed_tasks

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks
    )

if __name__ == "__main__":
    app.run(debug=True)