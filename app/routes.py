from app import app, db
from app.models import User, Recipe
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm, AddRecipeForm

@app.route('/')
def splash():
    return render_template('splash.html')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home', user=current_user)
    else:
        return redirect(url_for('splash'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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
        recipe = Recipe(name=form.recipe_name.data, directions=form.directions.data, ingredients=form.ingredients.data)
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe Added')
        return redirect(url_for('recipes'))
    return render_template('add_recipe.html', title='Add Recipe', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))