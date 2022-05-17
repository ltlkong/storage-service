from werkzeug.datastructures import FileStorage
from common.auth import ServiceAuth, Auth
from resources.BaseResource import BaseResource
from services.FileService import  create_file_service, FileService
from resources.BaseResource import BaseResource
from common.response import Response

auth=ServiceAuth()
auth_account=Auth()

class FileResource(BaseResource):
    # Get files data
    @auth.verify_key
    def get(self):
        self.parser.add_argument('storage_id',type=int,location='args', required=True, help='Storage id is required')
        self.parser.add_argument('name',type=str,location='args')
        self.parser.add_argument('type',type=str,location='args')
        self.parser.add_argument('public_key',type=str,location='args')
        args = self.parser.parse_args()

        file_service = create_file_service(args['storage_id'], auth.current_service())

        data = file_service.get(name=args['name'], type=args['type'], public_key=args['public_key'], with_internal_key=True)

        return Response.ok(data['message'], data = data['files'])

    # Upload file
    @auth.verify_key
    def post(self):
        self.parser.add_argument('storage_id',type=int,location='args', required=True, help='Storage id is required')
        self.parser.add_argument('previous_file_key',type=str,location='form')
        self.parser.add_argument('name',type=str,location='form')
        self.parser.add_argument('file',type=FileStorage,location='files', required=True, help='File is required')
        args = self.parser.parse_args()

        file_service = create_file_service(args['storage_id'], auth.current_service())

        data = file_service.upload(args['file'], args['previous_file_key'],args['name'])

        return Response.ok(data['message'], data = data['file'])

class FileOperationPublicResource(BaseResource):
    # Download file
    def get(self,file_key):
        data = FileService.download(public_key=file_key)

        return Response.file(data['path'])

class FileOperationResource(BaseResource):
    # Download file
    @auth_account.verify_token
    def get(self,file_key):
        data = FileService.download(internal_key=file_key)

        return Response.file(data['path'])
