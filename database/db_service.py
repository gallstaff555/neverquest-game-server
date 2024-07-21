#!/usr/bin/env

from sqlalchemy import create_engine, Table, Text, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

db_file = '../neverquest.db'
engine = create_engine(db_file, pool_size = 5, max_overflow = 10, echo=True)
Session = sessionmaker(bind=engine)
session_factory = scoped_session(Session)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    account_name = Column(Text)
    email = Column(Text)

Base.metadata.create_all(engine)

class DatabaseManager:
    def __init__(self):
        self.session = session_factory()

    def get_user_by_name(self, user_name):
        try:
            user = self.session.query(User).filter(User.id == user_name).first()
            return user
        except:
            self.session.rollback()
            print(f"Error retrieving account: {user_name}")
        finally:
            self.session.close()

    def add_user(self, user_name, email):
        try:
            new_user = User(user_name=user_name, email=email)
            self.session.add(new_user)
            self.session.commit()
            print(f"User: {user_name} created successfully")
        except Exception as e:
            self.session.rollback()
            print(f"Error adding user: {user_name}")
        finally:
            self.session.close()







# import sqlite3, threading

# DB = '../neverquest.db'

# class DBService:

#     def getAccountByName(self, accountName):
#         print("Getting account.")
#         conn = sqlite3.connect(DB)
#         cursor = conn.cursor()
#         res = cursor.execute('SELECT id FROM user_account WHERE account_name = (?)', (accountName,))
#         conn.commit()
#         accountId = res.fetchone()
#         if accountId is None:
#             print("Query returned no results")
#         else:
#             print(accountId)
#         print("Closing connection.")
#         conn.close()

#     def createNewAccount():



# if __name__ == '__main__':
#     print('asdf')
#     db = DBService()
#     db.getAccountByName('asdf')
