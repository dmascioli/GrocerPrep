from app import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    category = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Ingredient {}>'.format(self.name)
  
