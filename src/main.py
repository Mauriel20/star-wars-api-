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
from models import db, User
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








# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
