from werkzeug.datastructures import FileStorage
from common.auth import ServiceAuth
from resources.BaseResource import BaseResource
from services.FileService import  create_file_service
from resources.BaseResource import BaseResource
from common.response import Response

auth=ServiceAuth()

class FileResource(BaseResource):
    # Get files data
    @auth.verify_key
    def get(self):
        self.parser.add_argument('storage_id',type=int,location='args', required=True, help='Storage id is required')
        self.parser.add_argument('name',type=str,location='args')
        self.parser.add_argument('type',type=str,location='args')
        self.parser.add_argument('file_key',type=str,location='args')
        args = self.parser.parse_args()

        file_service = create_file_service(args['storage_id'], auth.current_service())

        data = file_service.get(name=args['name'], type=args['type'], key=args['file_key'])

        return Response.ok(data['message'], data = data['files'])

    # Upload file
    @auth.verify_key
    def post(self):
        self.parser.add_argument('storage_id',type=int,location='json', required=True, help='Storage id is required')
        self.parser.add_argument('previous_file_key',type=int,location='json')
        self.parser.add_argument('file',type=FileStorage,location='files', required=True, help='File is required')
        args = self.parser.parse_args()

        file_service = create_file_service(args['storage_id'], auth.current_service())

        data = file_service.upload(args['file'], args['previous_file_key'])

        return Response.ok(data['message'], data = data['file'])

class FileOperationResource(BaseResource):
    # Download file
    def get(self,storage_id, file_key):
        file_service = create_file_service(storage_id)

        data = file_service.download(file_key)

        return Response.file(data['path'])
