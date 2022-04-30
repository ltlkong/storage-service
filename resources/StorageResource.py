from werkzeug.datastructures import FileStorage
from common.core import ApiAuth
from resources.BaseResource import BaseResource
from services.StorageService import StorageService, create_storage_service, StorageType
from resources.BaseResource import BaseResource

api=ApiAuth()

class BaseStorageResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.storage_service:StorageService=create_storage_service(StorageType.local)

class StorageResource(BaseStorageResource):
    # Get files data
    @api.verify_api_key
    def get(self):
        self.parser.add_argument('name',type=str,location='args')
        self.parser.add_argument('type',type=str,location='args')
        received_data = self.parser.parse_args()
        name= received_data['name']
        type= received_data['type']

        return self.storage_service.get(api.internal_key, name=name, type=type)

    # Upload file
    @api.verify_api_key
    def post(self):
        self.parser.add_argument('file',type=FileStorage,location='files', required=True, help='File is required')
        received_data = self.parser.parse_args()
        file = received_data['file']

        return self.storage_service.store(file, api.internal_key)

class PublicStorageResource(BaseStorageResource):
    # Download file
    def get(self, file_key):
        return self.storage_service.get_file(file_key)
