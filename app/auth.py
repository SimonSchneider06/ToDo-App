from flask import request, Blueprint , render_template,flash,redirect ,url_for
from flask_login import login_required,login_user,logout_user
from .models import User
from app import db
from .help_functions import send_password_reset_email

auth = Blueprint("auth", __name__)

@auth.route("/sign_up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "POST":
        
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        rememberMe = request.form.get("rememberMe") #value is on or off

        #checkbox value is on or off -> needs to be converted to true or false
        if rememberMe == "on":
            rememberMe = True
        else:
            rememberMe = False

        user = User.query.filter_by(email = email).first()

        if user:
            flash("Email existiert bereits",category = "error")
            return redirect(url_for("auth.sign_up"))
        elif len(password1) < 7:
            flash("Das Passwort muss aus mindestens 7 Zeichen bestehen",category = "error")
            return redirect(url_for("auth.sign_up"))
        elif password1 != password2:
            flash("Die beiden Passwörter müssen übereinstimmen",category = "error")
            return redirect(url_for("auth.sign_up"))
        else:
            new_user = User(
                rememberMe = rememberMe,
                email = email,
                password = password1,
            )

            db.session.add(new_user)
            db.session.commit()

            flash("Erfolgreich Registriert",category = "success")
            login_user(new_user,remember = new_user.rememberMe)

            return redirect(url_for("task.home"))


    return render_template("auth/sign_up.html")

@auth.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first_or_404()

        if user.verify_password(password):
            
            login_user(user,remember = user.rememberMe)
            flash("Erfolgreich Angemeldet",category = "success")

            return redirect(url_for("task.home"))
        
        else:

            flash("Das Passwort ist nicht korrect",category = "error")
            return redirect(url_for("auth.login"))


    return render_template("auth/login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sie haben sich erfolgreich abgemeldet",category = "success")
    return redirect(url_for("auth.login"))

@auth.route("/forgot_password",methods = ["POST","GET"])
def password_reset():

    if request.method == "POST":
        email = request.form.get("email")

        if email == "":     #email field is empty
            flash("Bitte geben sie eine Email addresse ein",category="error")
            return redirect(url_for("auth.password_reset"))

        user = User.query.filter_by(email = email).first()

        if user:
            send_password_reset_email(user)

        flash("Ihnen wurde eine Email gesendet")

        return redirect(url_for("auth.password_reset"))

    return render_template("auth/password_reset.html")

@auth.route("/new_password/<token>", methods = ["POST","GET"])
def new_password(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('task.home'))
    
    user = User.verify_password_reset_token(token)
    #if token not verified
    if not user:
        return redirect(url_for("task.home"))
    
    if request.method == "POST":
        password1 = request.form.get("password")
        password2 = request.form.get("password2")

        if password1 == password2:
            user.password = password1
            db.session.commit()
            flash("Ihr Passwort wurde erfolgreich zurückgesetzt",category = "success")
            return redirect(url_for('task.home'))
        
    return render_template("auth/new_password.html")