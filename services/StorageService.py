from werkzeug.datastructures import FileStorage
from common.responses import error, success
import logging
from flask import current_app, send_from_directory, send_file
import os
from uuid import uuid4
from models.File import File
from models.ApiData import ApiData
import mimetypes

from utils.clear_none_in_dict import clear_none_in_dict

class StorageService:
    def store(self, file:FileStorage, api_internal_key):
        pass

    def get(self, api_internal_key, **kwargs):
        pass

    def get_file(self,file_key):
        pass

class LocalStorageService(StorageService):
    def __init__(self):
        self.dir = current_app.config['STORAGE_DIR']

    # Store a file to the storage dir
    def store(self, file:FileStorage, api_internal_key):
        if not file:
            return error('Internal error')

        api_data = ApiData.get(internal_key=api_internal_key)
        # Check if file types supported
        enabled_file_types = api_data.get_enabled_file_types()
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
            File.create(filename, key, file.mimetype, size, api_data.internal_key)
        except Exception as e:
            logging.error('Error saving file {}'.format(str(e)))

            return error('error')

        logging.info('File saved to {}'.format(path))
        
        return success('success',{ 'filename': filename, 'key': key, 'size':size, 'type': file.mimetype })

    # Get all files object from current api key
    def get(self, api_internal_key, **kwargs):
        new_kwargs = clear_none_in_dict(**kwargs)
        files = map(lambda f: f.dict(), File.get(api_data_key = api_internal_key, **new_kwargs))

        return success('Your files',list(files))

    # Get file
    def get_file(self, file_key):
        file = File.get(key=file_key)

        if file is None:
            return error('Error getting file {}'.format(file.name))
        
        return send_file(path_or_file=(self.generate_path(file.type) + file_key))

    def generate_path(self, dir:str):
        current_directory = os.getcwd() + self.dir
        final_directory = os.path.join(current_directory, r"" + dir)

        logging.info(current_directory + dir)

        if not os.path.exists(final_directory):
           os.makedirs(final_directory)

        return current_directory + dir + '/'
