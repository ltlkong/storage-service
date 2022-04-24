from werkzeug.datastructures import FileStorage
from common.core import ApiAuth, parse_args
from services.StorageService import StorageService, LocalStorageService
from flask_restful import Resource

api=ApiAuth()

class BaseStorageResource(Resource):
    def __init__(self):
        self.storage_service:StorageService=LocalStorageService()

class StorageResource(BaseStorageResource):
    @api.verify_api_key
    def get(self):
        request_data = parse_args(('name', str),('type',str))
        name= request_data['name']
        type= request_data['type']

        return self.storage_service.get(api.internal_key, name=name, type=type)

    @api.verify_api_key
    def post(self):
        request_data = parse_args(('file', FileStorage),location='files')
        file = request_data['file']

        return self.storage_service.store(file, api.internal_key)

class PublicStorageResource(BaseStorageResource):
    def get(self, file_key):
        return self.storage_service.get_file(file_key)
