from common.auth import Auth
from resources.BaseResource import BaseResource
from services.ApiService import ApiService
from common.response import Response

auth = Auth()

class ServiceResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.api_service = ApiService()

    # Get service data
    @auth.verify_token
    def get(self):
        self.parser.add_argument('name',type=str,location='args',required=False)
        args = self.parser.parse_args(strict=True)

        data = self.api_service.get_services(auth.current_user(), name=args['name'])

        return Response.ok(data=data)

        
    # Create service data
    @auth.verify_token
    def post(self):
        self.parser.add_argument('name',type=str,location='json',required=False)
        self.parser.add_argument('description',type=str,location='json',required=False)
        args = self.parser.parse_args(strict=True)

        data = self.api_service.create_service(auth.current_user(), name=args['name'], description=args['description'])

        return Response.created(data['message'], data['service'])
        

