#!/usr/bin/env python3

import sys
sys.path.append('..')
from flask import Flask, jsonify, request
from token_service import TokenService
from persistence.account_repository import DatabaseManager

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
            print(f"New char name: {new_char_name}")
            add_char_result = add_character(decoded_token['cognito:username'], decoded_token['email'], new_char_name)
            print(f"char res type: {type(add_char_result)}")
            characters_list = get_character_names(decoded_token['cognito:username'], decoded_token['email'])
            print(f"Result: {add_char_result}")
            if characters_list is None or add_char_result is None:
                print("No characters found or some other error occurred.")
                return jsonify({"name": [], "error": "Internal server error. No characters found"}), 500
            if 'error' in add_char_result:
                error_result = {"name": [characters_list], "error": add_char_result['error']}
                return jsonify(error_result), 500
            else:
                characters_list = {"name": [characters_list]}
                return jsonify(characters_list), 200
        else:
            return jsonify({"name": []}), 500
    except Exception as e:
        print(f"Exception raised while adding character name: {e}")

@app.route('/game/character', methods=['DELETE'])
def delete_character():
    decoded_token = decode_token(request)
    try:
        if decoded_token is not None:
            data = request.get_json()
            delete_char_name = data.get('CharName')
            my_characters = get_character_names(decoded_token['cognito:username'], decoded_token['email'])
            if delete_char_name not in my_characters or my_characters is None:
                print(f"Character name {delete_char_name} not found.")
                return None, 400
            else:
                delete_character_helper(decoded_token['cognito:username'], decoded_token['email'], delete_char_name)
                result = get_character_names(decoded_token['cognito:username'], decoded_token['email'])
                status_code = 200 if len(result) != len(my_characters) else 500
                return jsonify(result), status_code
        else:
            print(f"Error with auth token. Unable to delete character {delete_char_name}")
            return 400
    except Exception as e:
        print(f"Error deleting character {delete_char_name} due to {e}")

def delete_character_helper(user_id, email, delete_char_name):
    id = get_user_id(user_id, email)
    try:
        db.delete_character(id, delete_char_name)
    except Exception as e:
        print(f"Error deleting character {delete_char_name}")

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
        result = db.add_character(user_id, new_char_name)
        print(f"\n\nResult is {result}")
    except Exception as e:
        print(f"Error adding new character {new_char_name} due to exception {e}")
        result = None
    finally:
        return result

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

# For testing. Generally flask server will be started from main thread
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)

