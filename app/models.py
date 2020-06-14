from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    category = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Ingredient {}>'.format(self.name)
  
class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    
    _directions = db.Column(db.String, default='step')
    @property
    def directions(self):
        return [float(x) for x in self._directions.split(';')]
    @directions.setter
    def ratings(self, value):
        self._directions += ';%s' % value

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe-ingredient'
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    amount = db.Column(db.Integer)
    unit = db.Column(db.VARCHAR(45), nullable=False)
    recipes = db.relationship("Recipe", back_populates="ingredients")
    ingredients = db.relationship("Ingredient", back_populates="recipes")

#TODO: may need to change this to just have an association table for the user?
class UserPantry(db.Model):
    __tablename__ = 'user pantry'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    amount = db.Column(db.Integer)
    unit = db.Column(db.VARCHAR(45), nullable=False)
    ingredients = db.relationship("Ingredient")