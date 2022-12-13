from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #for validating the form data
from flask_bcrypt import Bcrypt
from flask_app.models import workout
import re # for regex to check for emails

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'workout'
    
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.workout = []
        
    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
        
    @staticmethod
    def validate_registration(form_data):
        valid = True
        if len(form_data["first_name"]) <2:
            valid = False
            flash("First name must be more than 2 characters", "register")
        if len(form_data["last_name"]) <2:
            valid = False
            flash("Last name must be more than 2 characters", "register")
        if not EMAIL_REGEX.match(form_data['email']):
            valid = False
            flash("Email is not correct", "register")
        email_data = {
            'email': form_data['email']
        }
        user_or_not = User.get_by_email(email_data)
        if user_or_not != None:
            valid = False
            flash("Email is already taken", "register")
        if len(form_data["password"]) <8:
            valid = False
            flash("Password must be more than 8 characters", "register")
        if form_data["password"] != form_data["confirm_password"]:
            valid = False
            flash("Passwords must be the same", "register")
        return valid
    
    @staticmethod
    def validate_login(form_data):
        email_data = {
            "email": form_data["email"]
        }
        user_or_not = User.get_by_email(email_data)
        if user_or_not == None:
            flash("Incorrect login either password or email is incorrect", "login")
            return False
        if not bcrypt.check_password_hash(user_or_not.password, form_data['password']):
            flash("Incorrect login either password or email is incorrect", "login")
            return False
        return user_or_not