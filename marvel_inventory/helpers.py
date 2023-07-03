from flask import request, jsonify
from functools import wraps
import secrets
import decimal
import requests
import json

from marvel_inventory.models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)
        
        if not token:
            return jsonify({'message':'Token is missing'}), 401

        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message':'Token is invalid'}), 401
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message':'Token is invalid'}), 401
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)

def description_generator(name):
    name = str(name)
    url = "https://marvel-heroic-api-unlock-the-mcu-legendary-characters.p.rapidapi.com/name"

    querystring = {"q": name}

    headers = {
        "X-RapidAPI-Key": "4150364e67mshd14a8c1aa2795d4p10d4c4jsnb57e2361fc4d",
        "X-RapidAPI-Host": "marvel-heroic-api-unlock-the-mcu-legendary-characters.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    return data[0]['description']

def movies_appeared_generator(name):
    name = str(name)
    url = "https://marvel-heroic-api-unlock-the-mcu-legendary-characters.p.rapidapi.com/name"

    querystring = {"q": name}

    headers = {
        "X-RapidAPI-Key": "4150364e67mshd14a8c1aa2795d4p10d4c4jsnb57e2361fc4d",
        "X-RapidAPI-Host": "marvel-heroic-api-unlock-the-mcu-legendary-characters.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    return data[0]['appearances'][0] + " " + data[0]['appearances'][1]
    
def super_power_generator(name):
    name = str(name)
    url = "https://marvel-heroic-api-unlock-the-mcu-legendary-characters.p.rapidapi.com/name"

    querystring = {"q": name}

    headers = {
        "X-RapidAPI-Key": "4150364e67mshd14a8c1aa2795d4p10d4c4jsnb57e2361fc4d",
        "X-RapidAPI-Host": "marvel-heroic-api-unlock-the-mcu-legendary-characters.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    return data[0]['powers']