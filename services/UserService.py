import logging
from uuid import uuid4
from common.responses import  success
from models.Storage import Storage
from models.User import User
from common.core import encrypt_md5, generate_token
from flask_restful import abort
from http import HTTPStatus
import re

class UserService:
    def register(self, email:str, password:str):
        if not self.verify_email(email):
            abort(HTTPStatus.BAD_REQUEST, message='Email is not valid')

        if not self.verify_password(password):
            abort(HTTPStatus.BAD_REQUEST, message='Password must be at least 8 characters')

        if User.get(email=email):
            abort(HTTPStatus.BAD_REQUEST, message='Email already exists')
            
        if not User.create(email,password):
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message='Failed to create user')
        
        logging.info('User created {}'.format(email))
        
        return success('Registration success', {
                           'email':email
                       }, 201)

    def login(self, email:str, password:str):
        hash_password = encrypt_md5(password)

        user = User.get(email=email, password=hash_password)

        if not user: 
            abort(HTTPStatus.BAD_REQUEST, message='Email or password is not valid')

        token = generate_token({
            'user_id': user.id
        },1)

        user.update(update_login=True)

        logging.info('User logged in {}'.format(email))

        return success('Login success',{
                           'token':token,
                           'exp': 3
                       })

    def verify_email(self, email:str) -> bool:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False

        return True
    
    def verify_password(self, password:str) -> bool:
        if len(password) < 8:
            return False

        return True


