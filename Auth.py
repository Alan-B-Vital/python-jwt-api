from flask_httpauth import HTTPTokenAuth
import jwt
from Database import db


class Token:
    @staticmethod
    def create(user_name):
        return jwt.encode({"user_name": user_name}, "secret", algorithm="HS256")


def add_user_token(user_name):
    new_token = Token.create(user_name)
    if db.add_user(user_name, new_token) is False:
        raise Exception('Error')
    return {'token': new_token}

if __name__ == "Auth":
    db.add_user('admin', jwt.encode({"user_name": "admin"}, "secret", algorithm="HS256"))
    auth = HTTPTokenAuth(scheme='Bearer')

    @auth.verify_token
    def verify_token(token):
        user_name = db.get_user_from_token(token)
        if user_name:
            return user_name