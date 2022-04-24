from werkzeug.datastructures import FileStorage
from common.responses import error, success
import logging
from flask import current_app, send_from_directory, send_file
import os
from uuid import uuid4
from models.File import File
from models.ApiData import ApiData
import mimetypes

class StorageService:
    def store(self, file:FileStorage, api_internal_key:str):
        pass
    def get(self, api_internal_key:str, filename =None, key = None, type=None):
        pass

class LocalStorageService(StorageService):
    def __init__(self):
        self.dir = current_app.config['STORAGE_DIR']

    def store(self, file:FileStorage, api_internal_key:str):
        if not file:
            return error('Internal error')

        # Check if file types supported
        enabled_file_types = ApiData.get(internal_key=api_internal_key).get_enabled_file_types()
        if enabled_file_types and file.mimetype not in enabled_file_types:
            return error('File type not supported {}'.format(file.mimetype))

        # Prepare file data
        filename = file.filename or '???'
        extension = mimetypes.guess_extension(file.mimetype) or ''
        key = str(uuid4()) + extension
        path = self.generate_path(file.mimetype) + key
        size = 0

        try:
            file.save(path)
            size = os.stat(path).st_size
            File.create(filename, key, file.mimetype, size)
        except Exception as e:
            logging.error('Error saving file {}'.format(str(e)))

            return error('error')

        logging.info('File saved to {}'.format(path))
        
        return success('success',{ 'filename': filename, 'key': key, 'size':size })

    def get(self, api_internal_key:str, filename =None, key = None, type=None):
        test_key = '87b13ffe-d41d-41cc-95b5-ce7fea7a6e59.jpg'

        return send_file(path_or_file=(self.generate_path('image/jpeg') + test_key))
        

    def generate_path(self, dir:str):
        current_directory = os.getcwd() + self.dir
        final_directory = os.path.join(current_directory, r"" + dir)

        logging.info(current_directory + dir)

        if not os.path.exists(final_directory):
           os.makedirs(final_directory)

        return current_directory + dir + '/'
