import sys
sys.dont_write_bytecode = True

from flask import render_template, redirect, request, session, flash

from flask_app.models.user_model import User

from flask_app import app, bcrypt

# ==========  HOME PAGE  ============
@app.route('/')
def index():
    return render_template("index.html")

# =======  REGISTER (POST ROUTE)  =========
@app.route('/create', methods=['POST'])
def register():
    # if there are errors:
    # We call the staticmethod on User model to VALIDATE
    if not User.validate_data(request.form):
        # redirect to the home page
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) 
    print("PW HASH =============>", pw_hash)
    # else no errors:
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    print("DATA ==============>", data)
    new_user_id = User.create_user(data)
    session['uid'] = new_user_id
    return redirect('/recipes')

# ========  LOGIN (POST ROUTE)  ==========
@app.route('/login', methods = ['POST'])
def login():
    # create a variable
    logged_in_user = User.validate_login(request.form)

    if not logged_in_user:
        return redirect('/')

    session['uid'] = logged_in_user.id
    print("UID ==================>", logged_in_user.id)

    return redirect('/recipes')

# ======== LOG OUT =========
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


