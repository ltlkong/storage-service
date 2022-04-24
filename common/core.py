from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse
from hashlib import md5
from functools import wraps
from flask import  current_app
import jwt
import logging
from common.responses import error
from datetime import datetime, timedelta

db = SQLAlchemy()

Model = db.Model

# Take array of tuples ( str, type)
def parse_args(*args, location='json'):
    parser = reqparse.RequestParser()

    for key, type in args:
        parser.add_argument(key, type=type, location=location)

    return parser.parse_args()
    
    
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


def verify_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        request_data = parse_args(('Authorization', str), location='headers')
        token = request_data['Authorization']

        if token is None:
            return error('Your are missing a token')

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

            if data['user_id']:
                return f(*args, **kwargs, user_id=data['user_id'])
                
            return error('Token is invalid')
        except jwt.ExpiredSignatureError as e:
            return error('Token has expired')
        except Exception as e:
            logging.error('Something went wrong while verify_token {}'.format(str(e)))

            return error('Token is invalid')

    return decorator


def verify_api_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        request_data = parse_args(('token', str))
        token = request_data['token']

        if token is None:
            return error('Your are missing a token')

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

            if data['user_id']:
                return f(*args, **kwargs, user_id=data['user_id'])
                
            return error('Token is invalid')
        except Exception as e:
            logging.error('Something went wrong while verify_token {}'.format(str(e)))

            return error('Token is invalid')

    return decorator

