import logging
from uuid import uuid4
from common.responses import  success
from models.Storage import Storage
from models.User import User
from common.core import encrypt_md5, generate_token
from utils.verify_email import verify_email
from flask_restful import abort

class UserService:
    def register(self, email:str, password:str):
        if not verify_email(email):
            abort(400, message='Email is not valid')

        if len(password) < 8:
            abort(400, message='Password must be at least 8 characters')

        if User.get(email=email):
            abort(400, message='Email already exists')
            
        if not User.create(email,password):
            abort(500, message='Failed to create user')
        
        logging.info('User created {}'.format(email))
        
        return success('Registration success', {
                           'email':email
                       }, 201)

    def login(self, email:str, password:str):
        hash_password = encrypt_md5(password)

        user = User.get(email=email, password=hash_password)

        if not user: 
            abort(400, message='Email or password is not valid')

        token = generate_token({
            'user_id': user.id
        },1)

        user.update(update_login=True)

        logging.info('User logged in {}'.format(email))

        return success('Login success',{
                           'token':token,
                           'exp': 3
                       })

