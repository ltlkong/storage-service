import logging
from common.responses import error, success
from models.User import User
from common.core import encrypt_md5, generate_token
from utils.verify_email import verify_email

class UserService:
    def register(self, email:str, password:str):
        if email is None or password is None:
            return error("Please provide email and password",400)

        if not verify_email(email):
            return error('Email invalid', 400)

        if len(password) < 8:
            return error('Password format incorrect',400)

        if User.get(email=email):
            return error('User already registered', 400)
            
        if not User.create(email,password):
            return error('Registration failed', 400)
        
        return success('Registration success', {
                           'email':email
                       }, 201)

    def login(self, email:str, password:str):
        if email is None or password is None:
            return error("Please provide email and password",400)

        hash_password = encrypt_md5(password)

        user = User.get(email=email, password=hash_password)

        if not user: 
            return error('Email or password incorrect', 401)

        token = generate_token({
            'user_id': user.id
        },3)

        user.update(update_login=True)

        return success('Login success',{
                           'token':token,
                           'exp': 3
                       })

    def generate_api_key(self, user_id):
        if user_id is None:
            logging.error('User id is required to generate_api_key')
            error('Internal error',500)

        key = generate_token({'user_id':user_id})

        user = User.get(id=user_id)

        if not user.update(key):
            return error('Error occurred while updating user api key',500)

        return success('API key generated', {
                           'key':key
                       })



