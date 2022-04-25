from flask_restful import Resource, reqparse
from common.core import parse_args, Auth
from services.UserService import UserService
from services.ApiService import ApiService

auth = Auth()

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
    def __init__(self):
        self.api_service = ApiService()

    @auth.verify_token
    def get(self):
        request_data = parse_args(('name', str), location='args')
        name = request_data['name']

        return self.api_service.get_api_data(user_id=auth.user_id, name=name)
        
    @auth.verify_token
    def post(self):
        request_data= {
            **parse_args(('enabled_file_types', str), action='append'),
            **parse_args(('name',str))
        }
        enabled_file_types = request_data['enabled_file_types']
        name = request_data['name']

        return self.api_service.generate_api_key(auth.user_id, name, enabled_file_types)
