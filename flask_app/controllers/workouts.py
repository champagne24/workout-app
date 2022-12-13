from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models import user, workout
from flask import flash

#visiable routes
@app.route('/workouts/new')
def new_workout():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('new_workout.html', this_user = user.User.get_one(data))

@app.route('/view/workout/<int:id>')
def view_one_workout(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    return render_template('view_one_workout.html', this_workout = workout.Workout.get_one_workout_with_user(data))

@app.route('/edit/workout/<int:id>')
def edit_workout(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    return render_template("edit_workout.html", this_workout = workout.Workout.get_one_workout_with_user(data))

#invisable route
@app.route('/user/delete/<int:id>')
def delete_workout(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    workout.Workout.delete_workout(data)
    return redirect('/home')

@app.route("/edit/workout/<int:id>/db", methods = ['POST'])
def edit_work_db(id):
    if 'user_id' not in session:
        return redirect('/')
    if not workout.Workout.validate_workout(request.form):
        return redirect(f"/edit/workout/{id}")
    data = {
        "workout": request.form["workout"],
        'description': request.form['description'],
        'date': request.form['date'],
        'day': request.form['day'],
        'id': id
    }
    workout.Workout.edit_workout(data)
    return redirect("/home")

@app.route('/workout/add_to_db', methods = ['POST'])
def add_workout_to_db():
    if 'user_id' not in session:
        return redirect('/')
    if not workout.Workout.validate_workout(request.form):
        return redirect('/paintings/new')
    data = {
        'workout': request.form['workout'],
        'description': request.form['description'],
        'date': request.form['date'],
        'day': request.form['day'],
        'user_id': session['user_id']
    }
    workout.Workout.add_workout(data)
    return redirect('/home')