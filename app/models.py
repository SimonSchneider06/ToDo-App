from . import db
from flask_login import UserMixin 
from sqlalchemy.sql import func 
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
from flask import current_app as app

# user class
class User(db.Model,UserMixin):
    #defining the tablename
    __tablename__ = "users"

    #user id
    id = db.Column(db.Integer,primary_key = True)

    #remember user after login
    rememberMe = db.Column(db.Boolean)

    #email and password
    email = db.Column(db.String(50), unique = True)
    password_hash = db.Column(db.String(50))

    #date added
    dateAdded = db.Column(db.DateTime(timezone = True),default = func.now())

    #relationships

    #note
    tasks = db.relationship("Task",backref = "user",lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self,password):
        #hash the input password
        self.password_hash = generate_password_hash(password,method="sha256")

    def verify_password(self,password):
        #verify if the given password matches the stored password
        return check_password_hash(self.password_hash,password)
    
    #generate password reset token for password reset throught email, to make it more secure
    def generate_password_reset_token(self,expiration = 600):
        return jwt.encode(
            {"reset_password":self.id,"exp":time() + expiration},app.config["SECRET_KEY"],algorithm="HS256"
        )
    
    #verify the token, returns user if exists else return none
    @staticmethod
    def verify_password_reset_token(token):
        try:
            id = jwt.decode(token,app.config["SECRET_KEY"],algorithms=["HS256"])["reset_password"]
        except:
            return
        return User.query.get(id)
    

# note
class Task(db.Model):

    __tablename__ = "tasks"

    #id
    id = db.Column(db.Integer,primary_key = True)

    #title
    title = db.Column(db.String(50))

    #text 
    text = db.Column(db.Text)

    #relationships

    #user
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))