from werkzeug.datastructures import FileStorage
from common.core import parse_args, auth
from services.StorageService import StorageService
from flask_restful import Resource

class BaseStorageResource(Resource):
    def __init__(self):
        self.storage_service=StorageService()

class StorageResource(BaseStorageResource):
    @auth.verify_api_key
    def post(self):
        request_data = parse_args(('file', FileStorage),location='files')
        file = request_data['file']

        return self.storage_service.store(file)
