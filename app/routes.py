from flask import Blueprint, render_template, request, redirect

from .models import db, Task

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        new_task = Task(
            title=title,
            description=description
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect("/")

    # -------------------------
    # Search
    # -------------------------

    search = request.args.get("search", "").strip()

    if search:

        tasks = Task.query.filter(
            Task.title.ilike(f"%{search}%")
        ).all()

    else:

        tasks = Task.query.all()

    # -------------------------
    # Dashboard Statistics
    # -------------------------

    total_tasks = Task.query.count()

    pending_tasks = Task.query.filter_by(
        status="Pending"
    ).count()

    completed_tasks = Task.query.filter_by(
        status="Completed"
    ).count()

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks
    )


@main.route("/delete/<int:id>")
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect("/")


@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    task = Task.query.get_or_404(id)

    if request.method == "POST":

        task.title = request.form["title"]
        task.description = request.form["description"]

        db.session.commit()

        return redirect("/")

    return render_template(
        "edit.html",
        task=task
    )


@main.route("/toggle/<int:id>")
def toggle_task(id):

    task = Task.query.get_or_404(id)

    if task.status == "Pending":
        task.status = "Completed"
    else:
        task.status = "Pending"

    db.session.commit()

    return redirect("/")