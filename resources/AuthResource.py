import uuid
from common.core import Auth
from services.UserService import UserService
from services.StorageService import StorageService
from resources.BaseResource import BaseResource
from services.ApiService import ApiService

auth = Auth()

class BaseAuthResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        self.api_service = ApiService()

class LoginResource(BaseAuthResource):
    # Login
    def post(self):
        self.parser.add_argument('email',type=str,location='json',required=True, help='Email is required')
        self.parser.add_argument('password',type=str,location='json',required=True, help='Password is required')
        received_data = self.parser.parse_args(strict=True)
        email = received_data['email']
        password = received_data['password']

        return self.user_service.login(email, password)

class RegisterResource(BaseAuthResource):
    # Register a new user
    def post(self):
        self.parser.add_argument('email',type=str,location='json',required=True, help='Email is required')
        self.parser.add_argument('password',type=str,location='json',required=True, help='Password is required')
        received_data = self.parser.parse_args(strict=True)
        email = received_data['email']
        password = received_data['password']

        return self.user_service.register(email, password)

class ApiAuthResource(BaseAuthResource):
    def __init__(self):
        super().__init__()
        self.storage_service = StorageService()

    # Get api key data
    @auth.verify_token
    def get(self):
        self.parser.add_argument('name',type=str,location='args')
        received_data = self.parser.parse_args()
        name = received_data['name']

        return self.api_service.get_storage_key(user_id=auth.user_id, name=name)
        
    # Create api key data
    @auth.verify_token
    def post(self):
        self.parser.add_argument('name',default=str(uuid.uuid4()) ,type=str)
        self.parser.add_argument('enabled_file_types',type=str, action='append')
        received_data = self.parser.parse_args()
        enabled_file_types = received_data['enabled_file_types']
        name = received_data['name']

        return self.api_service.generate_api_key(auth.user_id, name, enabled_file_types)
