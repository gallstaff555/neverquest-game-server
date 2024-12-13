#!/usr/bin/env python3 

import sys
sys.path.append('..')
from services.token_service import TokenService
from persistence.account_repository import DatabaseManager

tokenService = TokenService()
db = DatabaseManager()
debug=True

class AccountService():

    def delete_character_helper(self, user_id, email, delete_char_name):
        id = self.get_user_id(user_id, email)
        try:
            db.delete_character(id, delete_char_name)
        except Exception as e:
            print(f"Error deleting character {delete_char_name}")

    def get_character_names(self, user, email):
        id = self.get_user_id(user, email)
        my_character = db.get_characters(id)
        if my_character is None and debug:
            print(f"Error getting character. Value is None.")
        return my_character

    def get_user_id(self, user, email):
        try: 
            return db.get_user_id(user, email)
        except Exception as e:
            print(f"Error getting user id due to exception {e}")

    def add_character(self, user, email, new_char_name):
        try:
            user_id = self.get_user_id(user, email)
            result = db.add_character(user_id, new_char_name)
            print(f"Result is {result}")
        except Exception as e:
            print(f"Error adding new character {new_char_name} due to exception {e}")
            result = None
        finally:
            return result

