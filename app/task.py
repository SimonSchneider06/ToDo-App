from flask import Blueprint, render_template, redirect,url_for, request,flash
from flask_login import login_required
from .models import Task
from app import db
from flask_login import current_user

task = Blueprint("task",__name__)

@task.route("/add_new", methods = ["POST","GET"])
@login_required
def add_task():
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")

        if title == "" or text == "" or title == None or text == None:
            flash("Bitte füllen sie alle Felder aus", category = "error")
            print(title)
            print(text)
            return redirect(url_for("task.add_task"))

        else :
            new_task = Task(
                title = title,
                text = text,
                user_id = current_user.id
                )
            
            db.session.add(new_task)
            db.session.commit()

            flash("Erfolgreich neue Aufgabe hinzugefügt", category = "success")
            return redirect(url_for("task.home"))
        
    
    return render_template("task/add_task.html")

@task.route("/")
@login_required
def home():
    tasks = Task.query.filter_by(user_id = current_user.id).all()
    return render_template("task/home.html",tasks = tasks)


@task.route("/delete/<int:id>")
@login_required
def delete(id):

    task = Task.query.filter_by(id = id).first_or_404()

    try:
        db.session.delete(task)
        db.session.commit()
        flash("Aufgabe erfolgreich gelöscht", category = "success")
        return redirect(url_for("task.home"))
    
    except:
        flash("Es ist ein Fehler unterlaufen, bitte versuchen sie es erneut", category = "error")
        return redirect(url_for("task.home"))