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
        request_data = parse_args(('filename', str),('type',str))
        filename= request_data['filename']
        type= request_data['type']

        return self.storage_service.get(str(api.internal_key), filename, type)

    @api.verify_api_key
    def post(self):
        request_data = parse_args(('file', FileStorage),location='files')
        file = request_data['file']

        return self.storage_service.store(file, str(api.internal_key))
