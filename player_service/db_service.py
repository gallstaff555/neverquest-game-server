#!/usr/bin/env python3

from sqlalchemy import create_engine, Table, Text, Column, Integer, ForeignKey, event
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, relationship
from sqlite3 import Connection as SQLite3Connection

db_file = 'sqlite:///neverquest.db'
engine = create_engine(db_file, pool_size = 5, max_overflow = 10, echo=True)
Session = sessionmaker(bind=engine)
session_factory = scoped_session(Session)
Base = declarative_base()

@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column(Text)
    email = Column(Text)

class Characters(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

print("Creating tables that don't yet exist.")
Base.metadata.create_all(engine)

class DatabaseManager:
    def __init__(self):
        self.session = session_factory()

    def get_user_id(self, user_name, email):
        try:
            user = self.session.query(Users).filter(Users.user_name == user_name).first()
            if user is None:
                user = self.add_user(user_name, email)
            return user.id
        except Exception as e:
            self.session.rollback()
            print(f"[{self.__class__.__name__}] Error retrieving account: {user_name} due to exception {e}")
        finally:
            self.session.close()

    def add_user(self, user_name, email):
        try:
            new_user = Users(user_name=user_name, email=email)
            self.session.add(new_user)
            self.session.commit()
            print(f"[{self.__class__.__name__}] User: {user_name} created successfully")
            return new_user
        except Exception as e:
            self.session.rollback()
            print(f"[{self.__class__.__name__}] Error adding user: {user_name} due to exception {e}")
        finally:
            self.session.close()

    def get_characters(self, id):
        try:
            print(f"User id is {id}")
            characters = self.session.query(Characters).filter(Characters.user_id == id).all()
            #print(f"Here are my characters: {character_list[0]} and here is the type: {type(character_list)}")
            character_list = []
            for character in characters:
                character_list.append(character.name)
            return character_list
        except Exception as e:
            print(f"[{self.__class__.__name__}] Could not get character name due to exception {e}")
        finally:
            self.session.close()

    # TODO check for uniqueness
    def add_character(self, new_user_id, new_char_name):
        try:
            new_character = Characters(name=new_char_name, user_id=new_user_id)
            self.session.add(new_character)
            self.session.commit()
        except Exception as e:
            print(f"[{self.__class__.__name__}] Could not add new character due to exception {e}")
        finally:
            self.session.close()

    def delete_character(self, user_id, delete_char_name):
        try:
            delete_character = self.session.query(Characters).filter_by(name=delete_char_name, user_id=user_id).first()
            if delete_character:
                print(f"[{self.__class__.__name__}] Attempting to delete character {delete_char_name}.")
                self.session.delete(delete_character)
                self.session.commit()
                print(f"[{self.__class__.__name__}] Delete character {delete_char_name} successful.")
            else:
                print(f"[{self.__class__.__name__}] Character {delete_char_name} not found and won't be deleted.")
        except Exception as e:
            print(f"[{self.__class__.__name__}] Could not delete character {delete_char_name} due to {e}")
        finally:
            self.session.close()
