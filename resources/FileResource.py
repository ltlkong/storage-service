from werkzeug.datastructures import FileStorage
from common.auth import ServiceAuth
from resources.BaseResource import BaseResource
from services.StorageService import StorageService, create_storage_service, StorageType
from resources.BaseResource import BaseResource
from common.response import Response

auth=ServiceAuth()

class BaseStorageResource(BaseResource):
    def __init__(self):
        super().__init__()

class StorageResource(BaseStorageResource):
    # Get files data
    @auth.verify_key
    def get(self):
        self.parser.add_argument('storage_id',type=int,location='args')
        self.parser.add_argument('type',type=str,location='args')
        args = self.parser.parse_args()

        storage_service = create_storage_service(args['storage_id'], auth.current_service())

        data = storage_service.get(api.service, name=name, type=type)

        Response.ok(data['message'], data = data['storages'])

    # Upload file
    @auth.verify_key
    def post(self):
        self.parser.add_argument('file',type=FileStorage,location='files', required=True, help='File is required')
        received_data = self.parser.parse_args()
        file = received_data['file']

        return self.storage_service.store(file, api.service)

class PublicStorageResource(BaseStorageResource):
    # Download file
    def get(self, file_key):
        return self.storage_service.get_file(file_key)
