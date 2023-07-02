from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required, description_generator
from marvel_inventory.models import db, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def get(data):
    return {'some':'values'}

@api.route('/characters', methods=['POST'])
@token_required
def create_character(our_user):
    name = request.json['name']
    api_description = description_generator()
    movies_appeared = request.json['movies_appeared']
    super_power = request.json['super_power']
    date_created = request.json['date_created']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    character = Character(name, api_description, movies_appeared, super_power, date_created, user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_champion(our_user, id):
    if id:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message':'ID is missing'}), 401
    
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(our_user):
    token = our_user.token
    characters = Character.query.filter_by(user_token = token).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

@api.route('/characters/<id>', methods = ['PUT'])
@token_required
def update_character(our_user, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.description = description_generator()
    character.movies_appeared = request.json['movies_appeared']
    character.super_power = request.json['super_power']
    character.date_created = request.json['date_created']
    character.user_token = our_user.token

    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(our_user, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)