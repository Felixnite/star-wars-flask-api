from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(80), nullable=False)
    hair_color = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    favorites = db.relationship('Favorites', backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "gender": self.gender,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(80), nullable=False)
    diameter = db.Column(db.String(80), nullable=False)
    gravity = db.Column(db.String(80), nullable=False)
    weather = db.Column(db.String(80), nullable=False)
    favorites = db.relationship('Favorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "weather": self.weather,
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "characters_id": self.characters_id,
            "planets_id": self.planets_id,
        }    