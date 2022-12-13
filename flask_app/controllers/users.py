from flask import render_template, session, redirect, request
from flask_app import app
from flask_app.models import user, workout
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



#visible routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('home.html', this_user = user.User.get_one(data))



#Invisible

@app.route("/register",methods=['POST'])
def register_user():
    print(request.form)
    if not user.User.validate_registration(request.form):
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    session['user_id'] = user.User.register_user(data)
    
    return redirect('/home')

@app.route("/login", methods=['POST'])
def login():
    user_or_not = user.User.validate_login(request.form)
    if user_or_not == False:
        return redirect('/')
    session['user_id'] = user_or_not.id
    return redirect('/home')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')