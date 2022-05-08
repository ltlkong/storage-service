from werkzeug.datastructures import FileStorage
from common.auth import ServiceAuth
from resources.BaseResource import BaseResource
from services.StorageService import StorageService
from resources.BaseResource import BaseResource
from common.response import Response

auth=ServiceAuth()

class StorageResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.storage_service = StorageService()

    # Get all storages
    @auth.verify_key
    def get(self):
        self.parser.add_argument('name',type=str,location='args')
        self.parser.add_argument('type',type=str,location='args')
        args = self.parser.parse_args()

        data = self.storage_service.get(auth.current_service(), name=args['name'], type=args['type'])

        return Response.ok(data['message'], data = data['storages'])

    # Create storage
    @auth.verify_key
    def post(self):
        self.parser.add_argument('name',type=str, required=False)
        self.parser.add_argument('type',type=str, required=True)
        self.parser.add_argument('enabled_file_types',type=str, action='append', required=False)
        args = self.parser.parse_args()

        data = self.storage_service.create(auth.current_service(), name=args['name'], type=args['type'], enabled_file_types=args['enabled_file_types'])

        return Response.created(data['message'])
