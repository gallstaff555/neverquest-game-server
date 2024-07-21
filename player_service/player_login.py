#!/usr/bin/env python3

from flask import Flask, jsonify, request
from token_service import TokenService

tokenService = TokenService()
app = Flask(__name__)
debug=False

@app.route('/game/get_characters', methods=['POST'])
def refresh():
    data = request.get_json()
    id_token = data.get('IdToken')
    if debug:
        print(f"Id token: {id_token}")
    decoded_token = tokenService.verify_jwt(id_token)
    print(decoded_token)
    try:
        if decoded_token is not None:
            # TODO return list of characters instead of token values
            characters = {"name": ["gallstaff", "nomolos"]}
            return jsonify(characters), 200
        else:
            return None, 500
    except Exception as e:
        print(f"Exception raised: {e}")

def get_character_names():
    pass 
    # check if character names exist. If not, prompt player to enter new character name 

    # if characters exist 


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
