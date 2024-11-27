"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

Jose = {
    "first_name": "Jose",
    "age": 25,
    "lucky_numbers": [31, 7, 99]
}

Nacho = {
    "first_name": "Nacho",
    "age": 25,
    "lucky_numbers": [3, 20, 1]
}

Raul = {
    "first_name": "Raul",
    "age": 25,
    "lucky_numbers": [6,3,7]
}

Julian = {
    "first_name": "Julian",
    "age":28,
    "lucky_numbers": [23]
}

jackson_family.add_member(Jose)
jackson_family.add_member(Nacho)
jackson_family.add_member(Raul)
jackson_family.add_member(Julian)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['GET'])
def obtener_usuario():
    member = jackson_family.get_member(id)
    return jsonify(member), 200

@app.route('/members/', methods=['POST'])
def crear_usuario():
    member = request.json
    print('Añadiendo a ',member)
    jackson_family.add_member(member)
    if member is not None:
        return "miembro creado", 200

@app.route('/members/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    member = jackson_family.get_member(id)

    if member:
        jackson_family.delete_member(id)
        return jsonify({"Se ha borrado el usuario correctamente {member}"}), 200
    else:
        return jsonify({"Error, no se pudo encontrar un usuario con ese ID"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
