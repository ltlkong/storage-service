from werkzeug.datastructures import FileStorage
from common.response import  Response
import logging
from flask import current_app, send_from_directory, send_file
import os
from uuid import uuid4
from models.File import File
from models.Storage import Storage, StorageType
import mimetypes
from flask_restful import abort
from utils.clear_none_in_dict import clear_none_in_dict
from enum import Enum

# Abstract
class StorageService:
    def store(self, file:FileStorage, api_internal_key):
        pass

    def get(self, api_internal_key, **kwargs):
        pass

    def get_file(self,file_key):
        pass

# Factory
def create_storage_service(storage_id, service) -> StorageService:
    storage = Storage.query.filter_by(id = storage_id, service_id= service.id).first()

    if storage.type == StorageType.AMAZONS3:
        return S3StorageService(storage)
    else:
        return LocalStorageService(storage)

# Store files in server
class LocalStorageService(StorageService):
    def __init__(self, storage):
        self.dir = current_app.config['STORAGE_DIR']
        self.storage = storage

    # Store a file to the storage dir
    def store(self, file:FileStorage, api_internal_key):
        # Check if file types supported
        enabled_file_types = self.storage.get_enabled_file_types()
        file_type = file.mimetype.split('/')[0]

        if self.is_file_type_supported(file_type, enabled_file_types):
            abort(400, message='File type not supported')

        # Prepare file data
        filename = file.filename or '???'
        extension = mimetypes.guess_extension(file.mimetype) or ''
        key = str(uuid4()) + extension
        path = self.generate_path(file.mimetype) + key
        size = None

        try:
            file.save(path)
            size = os.stat(path).st_size
            File.create(filename, key, file.mimetype, size, self.storage.id)
        except Exception as e:
            logging.error('Error saving file {}'.format(str(e)))

            abort(500, message='Error saving file')

        logging.info('File saved to {}'.format(path))
        
        return Response.ok('success',{ 'filename': filename, 'key': key, 'size':size, 'type': file.mimetype })

    # Get all files object from current api key
    def get(self, api_internal_key, **kwargs):
        new_kwargs = clear_none_in_dict(**kwargs)
        files = map(lambda f: f.dict(), File.filter(storage_key = api_internal_key, **new_kwargs))

        return Response.ok('Your files',list(files))

    # Get file
    def get_file(self, file_key):
        file = File.get(key=file_key)

        if file is None:
            abort(404, message='File not found')
        
        return send_file(path_or_file=(self.generate_path(file.type) + file_key))

    def generate_path(self, dir:str):
        current_directory = os.getcwd() + self.dir
        final_directory = os.path.join(current_directory, r"" + dir)

        logging.info(current_directory + dir)

        if not os.path.exists(final_directory):
           os.makedirs(final_directory)

        return current_directory + dir + '/'

    def is_file_type_supported(self, file_type, allowed_file_types):
        return allowed_file_types and file_type not in allowed_file_types

class S3StorageService(StorageService):
    def __init__(self,storage):
        pass

    def store(self, file, api_internal_key):
        pass