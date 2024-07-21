#!/usr/bin/env python3

from flask import Flask, jsonify, request
from token_service import TokenService
from db_service import DatabaseManager

tokenService = TokenService()
db = DatabaseManager()
app = Flask(__name__)
debug=True

@app.route('/game/character', methods=['GET'])
def get_characters():
    decoded_token = decode_token(request)
    try:
        if decoded_token is not None:
            my_characters = get_character_names(decoded_token['cognito:username'], decoded_token['email'])
            if my_characters is None:
                print("Returning None.")
                return jsonify({"name": []}), 404
            else:
                result = {"name": [my_characters]}
                return jsonify(result), 200
        else:
            return jsonify({"name": []}), 500
    except Exception as e:
        print(f"Exception raised: {e}")

@app.route('/game/character', methods=['POST'])
def create_character():
    try:
        decoded_token = decode_token(request)
        if decoded_token is not None:
            data = request.get_json()
            new_char_name = data.get('NewCharName')
            print(f"\nNew char name: {new_char_name}")
            # make new character using decoded_token['cognito:username']
            add_character(decoded_token['cognito:username'], decoded_token['email'], new_char_name)
            # return list of all character belonging to account decoded_token['cognito:username']

            my_characters = get_character_names(decoded_token['cognito:username'], decoded_token['email'])

            print(f"\nMy chars: {my_characters}")
            if my_characters is None:
                print("Returning None.")
                return jsonify({"name": []}), 404
            else:
                result = {"name": [my_characters]}
                return jsonify(result), 200
        else:
            return jsonify({"name": []}), 500
    except Exception as e:
        print(f"Exception raised while adding character name: {e}")



def decode_token(request):
    try:
        data = request.get_json()
        id_token = data.get('IdToken')
        if debug:
            print(f"Id token: {id_token}")
        decoded_token = tokenService.verify_jwt(id_token)
        print(f"Decoded token: {decoded_token}")
        return decoded_token
    except Exception as e:
        print(f"Exception raised during token decoding: {e}")


def get_character_names(user, email):
    id = get_user_id(user, email)
    my_character = db.get_characters(id)
    if my_character is None and debug:
        print(f"Error getting character. Value is None.")
    return my_character

def get_user_id(user, email):
    try: 
        return db.get_user_id(user, email)
    except Exception as e:
        print(f"Error getting user id due to exception {e}")

def add_character(user, email, new_char_name):
    try:
        user_id = get_user_id(user, email)
        db.add_character(user_id, new_char_name)
    except Exception as e:
        print(f"Error adding new character {new_char_name} due to exception {e}")


# For testing. Generally flask server will be started from main thread
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)

# get public key from Cognito
# store time since public key last refreshed

# listen for requests from client
# refresh public key if needed
# validate request
# extract user email 

# if new login, add entry to database
# if existing user, fetch user's character names 
