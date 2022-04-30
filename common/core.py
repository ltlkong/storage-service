from os import abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort
from hashlib import md5
from functools import wraps
from flask import  current_app
import jwt
import logging
from http import HTTPStatus

db = SQLAlchemy()

Model = db.Model
    
def encrypt_md5(str:str):
    new_md5 = md5()
    new_md5.update(str.encode(encoding='utf-8'))

    return new_md5.hexdigest()

def generate_token(data, exp_hours=None):
    jwt_data = {
        **data
    }

    if exp_hours:
        jwt_data['exp_hours'] = exp_hours

    token = jwt.encode(jwt_data, current_app.config['SECRET_KEY'],algorithm='HS256')

    return token


class Auth:
    def __init__(self):
        self.user_id = None
        self.parser = reqparse.RequestParser()

    def verify_token(self,f):
        @wraps(f)
        def decorator(*args, **kwargs):
            # Getting token from header
            self.parser.add_argument('Authorization', str, location='headers', help='Token is required')
            received_data = self.parser.parse_args()

            token = received_data['Authorization']

            # Decoding token
            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                self.user_id = data['user_id']

            except jwt.ExpiredSignatureError as e:
                abort(HTTPStatus.UNAUTHORIZED, message='Token expired')
            except Exception as e:
                logging.error('Something went wrong while verify_token {}'.format(str(e)))

                abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')

            return f(*args, **kwargs)

        return decorator



class ApiAuth:
    def __init__(self):
        self.user_id = None
        self.internal_key = None
        self.parser = reqparse.RequestParser()

    def verify_api_key(self,f):
        @wraps(f)
        def decorator(*args, **kwargs):
            self.parser.add_argument('key', str, location='args', help='Key is required')
            received_data = self.parser.parse_args()
            key = received_data['key']

            try:
                data = jwt.decode(key, current_app.config['SECRET_KEY'], algorithms=['HS256'])

                self.user_id = data['user_id']
                self.internal_key = data['internal_key']

            except Exception as e:
                logging.error('Something went wrong {}'.format(str(e)))
                abort(HTTPStatus.UNAUTHORIZED)

            return f(*args, **kwargs)

        return decorator
