from common.auth import Auth
from services.AuthService import AuthService
from resources.BaseResource import BaseResource
from flask_restful import abort
from http import HTTPStatus
from common.response import Response
import logging

auth = Auth()

class BaseAuthResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()

class LoginType:
    ACCOUNT = 'account'
    REMEMBER_TOKEN = 'remember_token'

class LoginResource(BaseAuthResource):
    # Login
    def post(self, type):
        data = None

        if type == LoginType.ACCOUNT:
            self.parser.add_argument('email',type=str,location='json',required=True, help='Email is required')
            self.parser.add_argument('password',type=str,location='json',required=True, help='Password is required')
            self.parser.add_argument('remember',type=bool,location='json')
            args = self.parser.parse_args(strict=True)

            data = self.auth_service.loginWithAccount(args['email'],args['password'], args['remember'])

        elif type == LoginType.REMEMBER_TOKEN:
            self.parser.add_argument('token',type=str,location='json',required=True, help='Token is required')
            args = self.parser.parse_args(strict=True)

            data = self.auth_service.loginWithRememberToken(remember_token = args['token'])

        if data:
            return Response.ok(data['message'], data['login'])

        abort(HTTPStatus.NOT_FOUND)


class RegisterResource(BaseAuthResource):
    # Register a new user
    def post(self):
        self.parser.add_argument('email',type=str,location='json',required=True, help='Email is required')
        self.parser.add_argument('password',type=str,location='json',required=True, help='Password is required')
        args = self.parser.parse_args(strict=True)
        email = args['email']
        password = args['password']

        data = self.auth_service.register(email, password)

        return Response.created(data['message'])

class UserResource(BaseResource):
    # Check if user exists
    def get(self, email):
        pass

    # Handle request
    def post(self):
        # Deactivate user
        pass
