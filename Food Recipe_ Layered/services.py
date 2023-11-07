from flask_login import LoginManager, UserMixin, login_user
from models import Users, db, Recipe
from app import app


class UserService:
    def create_user(self, username, first_name, last_name, email, password):
        user = Users(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    def get_user_by_username(self, username):
        return Users.query.filter_by(username=username).first()

    def verify_password(self, user, password):
        return user.password == password

    def login_user(self, user):
        login_user(user)

# Define RecipeService in a similar manner

class RecipeServices:
     def create_recipe(self, title, instructions):
        recipe = Recipe(title=title, instructions=instructions)
        db.session.add(recipe)
        db.session.commit()

     def get_all_recipes(self):
        return Recipe.query.all()

     def get_recipe_by_id(self, recipe_id):
        return Recipe.query.get(recipe_id)

     def update_recipe(self, recipe_id, title, instructions):
        recipe = self.get_recipe_by_id(recipe_id)
        if recipe:
            recipe.title = title
            recipe.instructions = instructions
            db.session.commit()
        else:
            # Handle recipe not found
            return "Recipe not found"

     def delete_recipe(self, recipe_id):
        recipe = self.get_recipe_by_id(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
        else:
            # Handle recipe not found
            return "Recipe not found"


# Initialize LoginManager and db in app.py


# ... Other configurations ...
