from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from flask import  current_app
import jwt
from datetime import datetime, timedelta

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
        jwt_data['exp'] = datetime.now() + timedelta(hours=exp_hours)

    token = jwt.encode(jwt_data, current_app.config['SECRET_KEY'],algorithm='HS256')

    return token

class BasicStatus:
    ACTIVE = 'active'
    DISABLED = 'disabled'
