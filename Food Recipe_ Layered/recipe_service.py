from models import Recipe, db

class RecipeService:
    def get_all_recipes(self):
        return Recipe.query.all()

    def get_recipe_by_id(self, recipe_id):
        return Recipe.query.get(recipe_id)

    def create_recipe(self, title, instructions):
        recipe = Recipe(title=title, instructions=instructions)
        db.session.add(recipe)
        db.session.commit()

    def update_recipe(self, recipe_id, title, instructions):
        recipe = self.get_recipe_by_id(recipe_id)
        if recipe:
            recipe.title = title
            recipe.instructions = instructions
            db.session.commit()

    def delete_recipe(self, recipe_id):
        recipe = self.get_recipe_by_id(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
