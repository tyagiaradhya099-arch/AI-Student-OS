from flask import Flask, render_template, request

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        if "complete" in request.form:

            index = int(request.form["complete"])

            tasks[index]["done"] = True

        elif "delete" in request.form:

            index = int(request.form["delete"])

            tasks.pop(index)

        elif "clear" in request.form:

            tasks.clear()

        else:

            task = request.form["task"]

            tasks.append({
                "text": task,
                "done": False
            })

    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)