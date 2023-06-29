import sys
sys.dont_write_bytecode = True

from flask import render_template, redirect, request, session, flash

from flask_app.models.user_model import User

from flask_app.models.recipe_model import Recipe

from flask_app import app


# ==== DASHBOARD (Successful Login/Registration) ====

@app.route('/recipes')
def show_dashboard():

    if not "uid" in session:
        flash('ACCESS DENIED')
        return redirect('/')
    # retrieve user by ID
    data = {
        "id" : session['uid']
    }
    print("DATA ===============>", data)

    this_user = User.find_by_id(data)
    print("THIS USER =============>", this_user)

    all_recipes = Recipe.get_all()
    print("ALL RECIPES (CONTROLLER) =============>", all_recipes)

    return render_template("dashboard.html", this_user=this_user, all_recipes=all_recipes)


# ======== VIEW ONE RECIPE =========

@app.route('/recipes/<int:id>')
def view_recipe(id):
    data = {'id' : id}
    print("DATA ==========>", data)
    
    this_recipe = Recipe.get_one(data)

    data = {
        'id' : session['uid']
    }

    logged_in_user = User.find_by_id(data)

    return render_template('view_recipe.html', this_recipe = this_recipe, user=logged_in_user)


# =========  ADD A RECIPE PAGE  ===========

@app.route('/recipes/new')
def add_recipe():

    data = {
        "id" : session['uid']
    }

    this_user = User.find_by_id(data)

    print("THIS USER ID ===========>", this_user['id'])
    print("THIS USER  ===========>", this_user)
    print("THIS USER FIRST NAME ===========>", this_user['first_name'])

    return render_template('add_recipe.html', this_user=this_user)


# ========  ADD A RECIPE (POST ROUTE) =======
@app.route('/recipes/create', methods = ['POST'])
def new_recipe():
    if not Recipe.validate_data(request.form):
        return redirect('/recipes/new')
    print("REQUEST.FORM ===============>", request.form)
    new_recipe = Recipe.create_recipe(request.form)
    print("NEW RECIPE ===============>", new_recipe)

    return redirect('/recipes')


# =============  EDIT A RECIPE  ==============
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if not 'uid' in session:
        flash('Login to continue!')
        return redirect('/')

    data = {'id' : session['uid']}

    logged_in_user = User.find_by_id(data)

    recipe = Recipe.get_one({'id':id})

    return render_template('edit_recipe.html', user= logged_in_user, recipe=recipe)


# =========  EDIT A RECIPE (POST ROUTE) ===========
@app.route('/recipes/update/<int:id>', methods = ['POST'])
def update_recipe(id):

    data = {
        'id' : id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under_30mins' : request.form['under_30mins']
    }

    Recipe.update(data)
    return redirect('/recipes')



# =============   DELETE   =============
@app.route("/recipes/delete/<int:id>")
def delete(id):
    data = {"id":id}
    print("DATA TO DELETE (CONTROLLER)=================>", data)
    Recipe.delete(data)
    return redirect("/recipes")

