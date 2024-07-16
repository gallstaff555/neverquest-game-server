#!/usr/bin/env python3

from flask import Flask, Response, jsonify, request
import requests, boto3, jwt
from token_service import TokenService

token = TokenService()
app = Flask(__name__)

@app.route('/game/get_characters', methods=['POST'])
def refresh():
    data = request.get_json()
    id_token = data.get('IdToken')
    decoded_token = token.verify_jwt(id_token)
    if decoded_token is not None:
        # TODO return list of characters instead of token values
        characters = {"name": ["gallstaff", "nomolos"]}
        return jsonify(characters), 200
    else:
        return None, 500

# For testing. Generally flask server will be started from main thread
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False)

# get public key from Cognito
# store time since public key last refreshed

# listen for requests from client
# refresh public key if needed
# validate request
# extract user email 

# if new login, add entry to database
# if existing user, fetch user's character names 
