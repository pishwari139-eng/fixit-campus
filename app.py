import os

from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

problems = []


@app.route("/")
def home():
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()

    filtered_problems = problems

    if search:
        filtered_problems = [
            problem for problem in filtered_problems
            if search in problem["title"].lower()
            or search in problem["description"].lower()
            or search in problem["location"].lower()
        ]

    if category:
        filtered_problems = [
            problem for problem in filtered_problems
            if problem["category"] == category
        ]

    if status:
        filtered_problems = [
            problem for problem in filtered_problems
            if problem["status"] == status
        ]

    commit_id = os.environ.get(
        "RENDER_GIT_COMMIT",
        "Local Development"
    )

    return render_template(
        "index.html",
        problems=filtered_problems,
        search=search,
        selected_category=category,
        selected_status=status,
        commit_id=commit_id
    )


@app.route("/add", methods=["POST"])
def add_problem():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    location = request.form.get("location", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "").strip()

    if (
        not title
        or not category
        or not location
        or not description
        or not priority
    ):
        return "All fields are required", 400

    problem = {
        "title": title,
        "category": category,
        "location": location,
        "description": description,
        "priority": priority,
        "status": "Reported"
    }

    problems.append(problem)

    return redirect("/")


@app.route("/update-status/<int:problem_id>", methods=["POST"])
def update_status(problem_id):
    if problem_id < 0 or problem_id >= len(problems):
        return "Problem not found", 404

    new_status = request.form.get("status", "").strip()

    valid_statuses = ["Reported", "In Progress", "Resolved"]

    if new_status not in valid_statuses:
        return "Invalid status", 400

    problems[problem_id]["status"] = new_status

    return redirect("/")


@app.route("/api/problems")
def api_problems():
    return jsonify(problems)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
