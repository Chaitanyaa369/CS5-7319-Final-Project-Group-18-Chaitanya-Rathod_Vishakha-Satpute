from flask import Flask, render_template, url_for, redirect, flash, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import Users, Recipe, db
#from sql import user_data
#from form import IngredientSearchForm
from datetime import datetime
import json
import requests


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres1@localhost/flask_db"
app.config["SECRET_KEY"] = "abc"



login_manager = LoginManager()
login_manager.init_app(app)




db.init_app(app)


with app.app_context():
	db.create_all()


SPOONACULAR_API_KEY = 'f272fbfb2cb244d598bc0420d4495e7a'

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		user = Users(username=request.form.get("username"), 
			   		first_name=request.form.get("first_name"),
					last_name=request.form.get("last_name"),
					email=request.form.get("email"),
					password=request.form.get("password"))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("sign_up.html")


@app.route("/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		if user.password == request.form.get("password"):
			login_user(user)
			return redirect(url_for("home"))
	return render_template("login.html")


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))


#@app.route('/profile')
#@login_required
#def profile():
 #   users = user_data()  # Call the function to get user data
  #  return render_template('profile.html', users=users)



@app.route("/recipe_manager", methods=['Get','POST'])
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.instructions = request.form['instructions']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/delete_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if request.method == 'POST':
        db.session.delete(recipe)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('delete_recipe.html', recipe=recipe)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        instructions = request.form['instructions']
        recipe = Recipe(title=title, instructions=instructions)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_recipe.html')

@app.route('/search', methods=['GET','POST'])
def search_recipe():
    ingredient1 = request.form.get('ingredient1')
    ingredient2 = request.form.get('ingredient2')
    ingredient3 = request.form.get('ingredient3')
    ingredient4 = request.form.get('ingredient4')

    # Search for recipes using the Spoonacular API
    endpoint = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'ingredients': f"{ingredient1},{ingredient2},{ingredient3},{ingredient4}",
        'instructions': 'true'
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        recipes = response.json()
    else:
        # Handle API request error
        return "Error: Unable to fetch recipes from the API"

    return render_template('results.html', recipes=recipes)

@app.route("/login",  methods=['GET', 'POST'])
def home():
	return render_template("home.html")

if __name__ == "__main__":
	app.run(debug=True)
