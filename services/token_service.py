#!/usr/bin/env python3

import boto3, requests, jwt, json

with open('configuration/secrets.json', 'r') as file:
    data = json.load(file)

debug=False

USER_POOL_ID = data.get('user_pool_id')
REGION = data.get('region')
AUDIENCE = data.get('audience')

class TokenService():

    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name=REGION)
    
    def refresh_public_key(self):
        try:
            response = self.client.describe_user_pool(UserPoolId=USER_POOL_ID)
            jwks_uri = f'https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json' 
            response = requests.get(jwks_uri)
            return response.json()
        except Exception as e: 
            print(f"\nError getting public key due to exception {e}.\nCheck AWS credentials are valid.")
    
    def verify_jwt(self, id_token):
        try:
            header = jwt.get_unverified_header(id_token)
            print(header)
        except jwt.JWTError as e:
            print(f'Error reading id token: {e}')

        jwks = self.refresh_public_key()
        print(f"jwks type: {type(jwks)}")
        print(f"\njwks: {jwks}\n")

        for key in jwks['keys']:
            if debug:
                print(f"\nkey: {key}\n")
            if key['kid'] == header['kid']:
                if debug:
                    print("keys matched!")
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                break
            else:
                print("kid did not match.")

        if not public_key:
            raise ValueError('Unable to find public key for verification.')
        else:
            try:
                decoded_token = jwt.decode(id_token, 
                                           key=public_key,
                                           audience=AUDIENCE,
                                           algorithms=["RS256"])
                print(f"\nDecoded token: {decoded_token}\n")
                return decoded_token
                #return json.dumps(decoded_token)
            except jwt.ExpiredSignatureError:
                print('Token is expired.')
                return None 
            except jwt.ImmatureSignatureError:
                print('Token is not valid yet (issued in the future)')
                return None
            except jwt.PyJWTError as e:
                print(f'JWT Error: {e}')
                return None 
            

    def decode_token(self, data):
        try:
            id_token = data.get('IdToken')
            if debug:
                print(f"Id token: {id_token}")
            decoded_token = self.verify_jwt(id_token)
            print(f"Decoded token: {decoded_token}")
            return decoded_token
        except Exception as e:
            print(f"Exception raised during token decoding: {e}")
        
