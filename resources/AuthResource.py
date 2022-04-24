from flask_restful import Resource
from common.core import parse_args, auth
from services.UserService import UserService

class BaseAuthResource(Resource):
    def __init__(self):
        self.user_service = UserService()
    

class LoginResource(BaseAuthResource):
    def post(self):
        request_data= parse_args(('email', str), ('password', str))
        email = request_data['email']
        password = request_data['password']

        return self.user_service.login(email, password)

class RegisterResource(BaseAuthResource):
    def post(self):
        request_data= parse_args(('email', str), ('password', str))
        email = request_data['email']
        password = request_data['password']

        return self.user_service.register(email, password)

class ApiAuthResource(BaseAuthResource):
    @auth.verify_token
    def post(self):
        return self.user_service.generate_api_key(auth.user_id)
        

        
