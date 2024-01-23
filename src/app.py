"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# Get all Characters


@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    people = list(map(lambda x: x.serialize(), people))
    return jsonify(people), 200

# Get a one single people information

@app.route('/<int:people_id>', methods=['GET'])
def get_one_people(id):
    people = People.query.get(id)
    if people is None:
        return jsonify({"message":"Character not found"}), 404   
    return jsonify(people.serialize()), 200

# Get a list of all the planets in the database.

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(planets), 200

# Get one single planet's information.

@app.route('/<int:planets_id>', methods=['GET'])
def get_one_planet(id):
    planets = Planets.query.get(id)
    if planets is None:
        return jsonify({"message":"Planet not found"}), 404   
    return jsonify(planets.serialize()), 200

# Get a list of all the blog post users.

@app.route('/users', methods=['GET'])
def get_all_users():
    user = User.query.all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user), 200

#  Get all the favorites that belong to the current user.

@app.route('/users/favorites/<int:theid>', methods=['GET'])
def get_user_favorites(theid=None):
    user = User.query.filter_by(id=theid).first()
    return jsonify(user.serialize()), 200

# Add a new favorite planet and people to the current user with the planet and people id 

@app.route('/favorites/people/<int:theid>', methods=['POST'])
def add_people_favorite(theid=None):
    request_body = request.get_json()
    user = User.query.get(request_body["user_id"])
    if user is None:
        raise APIException('User not found', status_code=404)
    people = People.query.get(theid)
    if people is None:
        raise APIException('People not found', status_code=404)
    favorites = Favorites()
    favorites.user_id = request_body["user_id"]
    favorites.people_id = theid
    db.session.add(favorites)
    db.session.commit()
    return jsonify("ok"), 200


@app.route('/favorites/planets/<int:theid>', methods=['POST'])
def add_planets_favorite(theid=None):
    request_body = request.get_json()
    user = User.query.get(request_body["user_id"])
    if user is None:
        raise APIException('User not found', status_code=404)
    planets = Planets.query.get(theid)
    if planets is None:
        raise APIException('Planets not found', status_code=404)
    favorites = Favorites()
    favorites.user_id = request_body["user_id"]
    favorites.planet_id = theid
    db.session.add(favorites)
    db.session.commit()
    return jsonify("ok"), 200

# Delete favorite planet and people


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite_people = Favorites.query.filter_by(people_id=people_id).first()
    if favorite_people is None:
        return jsonify({"message": "Favorite person not found"}), 404
    db.session.delete(favorite_people)
    db.session.commit()
    return jsonify("Favorite person deleted successfully"), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet = Favorites.query.filter_by(planet_id=planet_id).first()
    if favorite_planet is None:
        return jsonify({"message": "Favorite planet not found"}), 404
    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify("Favorite planet deleted successfully"), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
