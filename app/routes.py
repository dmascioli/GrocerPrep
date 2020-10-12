from app import app, db
from app.models import User, Recipe, Ingredient, RecipeIngredient, MealList, RecipeList
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, AddRecipeForm


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/home')
def home():
    if current_user.is_authenticated:
        meal_lists = MealList.query.filter_by(user_id=current_user.id).all()
        return render_template('home.html', title='Home', user=current_user, meal_lists=meal_lists)
    else:
        return redirect(url_for('splash'))


@app.route('/recipes/<int:recipe_id>')
@app.route('/recipes', methods=['GET'])
def recipes(recipe_id=None):
    if recipe_id is None:
        return render_template('recipes.html', recipes=Recipe.query.all())

    recipe = Recipe.query.filter_by(id=recipe_id).first()
    return render_template('recipe_view.html', recipe=recipe)


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = AddRecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(name=form.recipe_name.data,
                        directions=form.directions.data)

        ingredients = parse_ingredients(form.ingredients.data)
        db.session.add(recipe)
        db.session.commit()

        # last added recipe id
        recipe_id = Recipe.query.order_by(Recipe.id.desc()).first().id

        # add all ingredients to RecipeIngredient table
        for ingredient in ingredients:
            db.session.add(RecipeIngredient(
                recipe_id=recipe_id, ingredient_id=ingredient['id'], amount=ingredient['amount'], unit=ingredient['unit']))
        db.session.commit()

        flash('Recipe Added')
        return redirect(url_for('recipes'))
    return render_template('add_recipe.html', title='Add Recipe', form=form)


def parse_ingredients(ingredients):

    return_list = []

    ing_list = ingredients.split('\r\n')

    for ing in ing_list:

        # check database if this ingredient exists already
        # use api to get nutritional data
        ingredient = Ingredient(name=ing, serving_amount=am, serving_unit=unit,
                                calories=calories, carbs=carbs, protein=protein, fat=fat)
        db.session.add(ingredient)
        db.session.commit()

        ingredient_dict = {'id': Ingredient.query.order_by(
            Ingredient.id.desc()).first().id, 'amount': am, 'unit': unit}
        return_list.append(ingredient_dict)

    return return_list


@app.route('/create_list', methods=['GET', 'POST'])
def create_list():
    recipes = Recipe.query.all()
    if request.method == 'GET':
        return render_template('create_meal_list.html', recipes=recipes)
    else:
        selected_recipes = request.form.getlist('recipes')
        name = request.form.get('listname')
        list_entry = MealList(user_id=current_user.id, list_name=name)
        db.session.add(list_entry)
        db.session.flush()
        for id in selected_recipes:
            entry = RecipeList(list_id=list_entry.list_id, recipe_id=id)
            db.session.add(entry)
            db.session.commit()
        flash('Meal List created')
        return redirect(url_for('home'))


@app.route('/edit_list')
def edit_list():
    pass
