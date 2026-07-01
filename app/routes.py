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

    tasks = Task.query.all()

    return render_template(
        "index.html",
        tasks=tasks
    )
@main.route("/delete/<int:id>")
def delete_task(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)

    db.session.commit()

    return redirect("/")