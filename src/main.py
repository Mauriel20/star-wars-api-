"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
import json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

# Para user 

# get ejemplo explicado por San Tomas y amigos maravillosos jajaj xd
@app.route('/ejemplo', methods=['GET'])
def get_user():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# mi primer get a pata 
@app.route('/user', methods=['GET'])
def get_users():
    user = User.query.all()
    mapeo= list(map(lambda x: x.serialize(),user))
    return jsonify(mapeo), 200

# Get por id
@app.route('/user/<int:id_get>', methods=['GET'])
def get_with_id(id_get):
    usuario = User.query.get(id_get)
    usuario_final= usuario.serialize()
    return jsonify(usuario_final), 200

@app.route('/user', methods=['POST'])
def add_user():
   
    request_body = json.loads(request.data)

    if request_body["name"] == None and request_body["email"] == None and request_body["password"] == None:
        return "Datos incompletos"
    else:

        user = User(name=request_body["name"], email=request_body["email"], password=request_body["password"])
        db.session.add(user)
        db.session.commit()
        return "Posteo exitoso"
    
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user_by_id(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return("User has been deleted successfully"), 200

# @app.route('/user/<int:id>', methods=['DELETE'])
# def delete_user_by_id(id):
#     user = User.query.filter_by(id=id).first_or_404()
#     db.session.delete(user)
#     db.session.commit()
#     return("User has been deleted successfully"), 200

# para favoritos

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorite = Favorites.query.all()
    resultado = list(map(lambda x: x.serialize(),favorite))
    return jsonify(resultado)

@app.route('/favorites/<int:id>', methods=['GET'])
def get_favorites_by_id(id):
    favorito = Favorites.query.get(id)
    favorito_final= favorito.serialize()
    return jsonify(favorito_final),200 

@app.route('/favorites', methods=['POST'])
def add_favorites():
    request_body = json.loads(request.data)
    # if request_body["name"] == None and request_body["Type"] == None:
    if request_body["name"] == None:
        return "Hay datos incompletos, favor completarlos todos!"
    else:
        # return request_body["name"]
        # favorite = Favorites(name=request_body["name"], Type=request_body["Type"])
        favorite = Favorites(name=request_body["name"])
        db.session.add(favorite)
        db.session.commit()
        return "Posteo exitoso"

# def add_user():
   
#     request_body = json.loads(request.data)

#     if request_body["name"] == None and request_body["email"] == None and request_body["password"] == None:
#         return "Datos incompletos"
#     else:

#         user = User(name=request_body["name"], email=request_body["email"], password=request_body["password"])
#         db.session.add(user)
#         db.session.commit()
#         return "Posteo exitoso"






@app.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorites_by_id(id):
    favorite = Favorites.query.filter_by(id=id).first_or_404()
    db.session.delete(favorite)
    db.session.commit()
    return("User has been deleted successfully"), 200

# para DE CHARACTER

@app.route('/character', methods=['GET'])
def get_character():
    character = Character.query.all()

    resultado = list(map(lambda x: x.serialize(),character))
    return jsonify(resultado)

@app.route('/character/<int:id>', methods=['GET'])
# def get_character_by_id(id):
#     character = Character.query.filter_by(id=id).first_or_404()
#     return jsonify(character.serialize()) 
def get_character_by_id(id):
    character = Character.query.get(id)
    character_final= character.serialize()
    return jsonify(character_final),200 

@app.route('/character', methods=['POST'])
def add_character():
    request_body = json.loads(request.data)
    # if request_body["name"] == None and request_body["Type"] == None:
    if request_body["name"] == None and request_body["hair_color"] == None and request_body["skin_color"] == None and request_body["eyes_color"] == None and request_body["birth_day"] == None:
        return "Hay datos incompletos, favor completarlos todos!"
    else:
        # return request_body["name"]
        # favorite = Favorites(name=request_body["name"], Type=request_body["Type"])
        character = Character(name=request_body["name"], hair_color = request_body["hair_color"], skin_color = request_body["skin_color"], eyes_color = request_body["eyes_color"], birth_day = request_body["birth_day"]    )
        db.session.add(character)
        db.session.commit()
        return "Posteo exitoso"

# @app.route('/character/<int:id>', methods=['DELETE'])
# def delete_character_by_id(id):
#     character = Character.query.filter_by(id=id).first_or_404()
#     db.session.delete(character)
#     db.session.commit()
#     return("User has been deleted successfully"), 200

# Para PLANETS

@app.route('/planets', methods=['GET'])
def get_planet():
    planet = Planets.query.all()
    resultado = list(map(lambda x: x.serialize(), planet))
    return jsonify(resultado)

@app.route('/planets/<int:id_planet>', methods=['GET'])
# def get_planet_by_id(id):
#     planet = Planets.query.filter_by(id=id).first_or_404() 
#     return jsonify(planet.serialize())

def get_planets_by_id(id_planet):
    planets = Planets.query.get(id_planet)
    planets_final = planets.serialize()
    return jsonify(planets_final),200 

@app.route('/planets', methods=['POST'])
def add_planets():
    request_body = json.loads(request.data)
    # if request_body["name"] == None and request_body["Type"] == None:
    if request_body["name"] == None and request_body["rotation_period"] == None and request_body["orbital_period"] == None and request_body["terrain"] == None:
        return "Hay datos incompletos, favor completarlos todos!"
    else:
        # return request_body["name"]
        # favorite = Favorites(name=request_body["name"], Type=request_body["Type"])
        planets = Planets(name=request_body["name"], rotation_period = request_body["rotation_period"], orbital_period = request_body["orbital_period"], terrain = request_body["terrain"])
        db.session.add(planets)
        db.session.commit()
        return "Posteo exitoso"
    
# @app.route('/planets/<int:id>', methods=['DELETE'])
# def delete_planets_by_id(id):
#     planets = Planets.query.filter_by(id=id).first_or_404()
#     db.session.delete(planets)
#     db.session.commit()
#     return("User has been deleted successfully"), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
