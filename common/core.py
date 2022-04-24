from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse
from hashlib import md5
from functools import wraps
from flask import  current_app
import jwt
import logging
from common.responses import error

db = SQLAlchemy()

Model = db.Model

# Take array of tuples ( str, type)
def parse_args(*args, **kwargs):
    parser = reqparse.RequestParser()

    for key, type in args:
        parser.add_argument(key, type=type, required=False, **kwargs)

    return parser.parse_args()
    
    
def encrypt_md5(str:str):
    new_md5 = md5()
    new_md5.update(str.encode(encoding='utf-8'))

    return new_md5.hexdigest()

# TODO: Allow  file types
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

    def verify_token(self,f):
        @wraps(f)
        def decorator(*args, **kwargs):
            request_data = parse_args(('Authorization', str), location='headers')
            token = request_data['Authorization']

            if token is None:
                return error('Your are missing a token')

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

                if data['user_id']:
                    self.user_id = data['user_id']

                    return f(*args, **kwargs)
                    
                return error('Token is invalid')
            except jwt.ExpiredSignatureError as e:
                return error('Token has expired')
            except Exception as e:
                logging.error('Something went wrong while verify_token {}'.format(str(e)))

                return error('Token is invalid')

        return decorator



class ApiAuth:
    def __init__(self):
        self.user_id = None
        self.internal_key = None

    def verify_api_key(self,f):
        @wraps(f)
        def decorator(*args, **kwargs):
            request_data = parse_args(('key', str), location='args')
            key = request_data['key']

            if key is None:
                return error('Your are missing a key')

            try:
                data = jwt.decode(key, current_app.config['SECRET_KEY'], algorithms=['HS256'])

                if data['user_id'] and data['internal_key']:
                    self.user_id = data['user_id']
                    self.internal_key = data['internal_key']
                    return f(*args, **kwargs)
                    
                return error('Key is invalid')
            except Exception as e:
                logging.error('Something went wrong while verify_key {}'.format(str(e)))

                return error('Key is invalid')

        return decorator
