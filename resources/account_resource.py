#!/usr/bin/env python3

import sys
sys.path.append('..')
from flask import Blueprint, jsonify, request
from services.account_service import AccountService
from services.token_service import TokenService
from persistence.account_repository import DatabaseManager

account = AccountService()
tokenService = TokenService()
db = DatabaseManager()
main_bp = Blueprint('main', __name__)
debug=True

@main_bp.route('/game/character', methods=['GET'])
def get_characters():
    decoded_token = tokenService.decode_token(request.get_json())
    try:
        if decoded_token is not None:
            my_characters = account.get_character_names(decoded_token['cognito:username'], decoded_token['email'])
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

@main_bp.route('/game/character', methods=['POST'])
def create_character():
    try:
        decoded_token = tokenService.decode_token(request.get_json())
        if decoded_token is not None:
            data = request.get_json()
            new_char_name = data.get('NewCharName')
            print(f"New char name: {new_char_name}")
            add_char_result = account.add_character(decoded_token['cognito:username'], decoded_token['email'], new_char_name)
            print(f"char res type: {type(add_char_result)}")
            characters_list = account.get_character_names(decoded_token['cognito:username'], decoded_token['email'])
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

@main_bp.route('/game/character', methods=['DELETE'])
def delete_character():
    decoded_token = tokenService.decode_token(request.get_json())
    try:
        if decoded_token is not None:
            data = request.get_json()
            delete_char_name = data.get('CharName')
            my_characters = account.get_character_names(decoded_token['cognito:username'], decoded_token['email'])
            if delete_char_name not in my_characters or my_characters is None:
                print(f"Character name {delete_char_name} not found.")
                return None, 400
            else:
                account.delete_character_helper(decoded_token['cognito:username'], decoded_token['email'], delete_char_name)
                result = account.get_character_names(decoded_token['cognito:username'], decoded_token['email'])
                status_code = 200 if len(result) != len(my_characters) else 500
                return jsonify(result), status_code
        else:
            print(f"Error with auth token. Unable to delete character {delete_char_name}")
            return 400
    except Exception as e:
        print(f"Error deleting character {delete_char_name} due to {e}")



