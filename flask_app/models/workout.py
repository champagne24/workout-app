from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Workout:
    db_name = 'workout'
    
    def __init__(self,data):
        self.id = data["id"]
        self.workout = data["workout"]
        self.description = data["description"]
        self.date = data["date"]
        self.day = data["day"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user= None
        
    @classmethod
    def add_workout(cls,data):
        query = "INSERT INTO workouts (workout, description, date, day, user_id) VALUES (%(workout)s, %(description)s, %(date)s, %(day)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def edit_workout(cls,data):
        query = "UPDATE workouts SET workout = %(workout)s, description = %(description)s, date = %(date)s, day = %(day)s WHERE id = %(id);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete_workout(cls,data):
        query = "DELETE FROM workouts WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_one_workout_with_user(cls,data):
        query = "SELECT * FROM workouts JOIN users ON workouts.user_id = users.id WHERE workouts.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        if len(results) == 0:
            return None
        else:
            this_workout_object = cls(results[0])
            this_user_dictionary = {
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'password': results[0]['password'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at'],
            }
            this_user_object = user.User(this_user_dictionary)
            this_workout_object.user = this_user_object
            return this_workout_object
        

    @staticmethod
    def validate_workout(form_data):
        valid = True
        print(form_data)
        
        if len(form_data["workout"]) <3:
            valid = False
            flash("Workout must be 3 or more letters")
        if len(form_data["description"]) <6:
            valid = False
            flash("Description must be 6 or more letters")
        if len(form_data["day"]) >3:
            valid = False
            flash("Day must be 3 or more letters")
        return valid