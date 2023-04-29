from functools import wraps 
from flask import abort,render_template
from flask_login import current_user
from flask_mail import Message
from flask import current_app as app
from app import mail


#adding errors to app
def errorhandling_init(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error.html"),404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("error.html"),500
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("error.html"),403
    
#-------------mail sending-----------------------
def send_mail(to,subject,template,**kwargs):
    msg = Message(app.config["MAIL_PREFIX"] + subject, sender = app.config["MAIL_USERNAME"],recipients=[to])
    msg.body = render_template(template + ".txt",**kwargs)
    msg.html = render_template(template + ".html",**kwargs)
    mail.send(msg)