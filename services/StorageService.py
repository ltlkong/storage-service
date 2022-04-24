from werkzeug.datastructures import FileStorage
from common.responses import error, success
import logging
from flask import current_app
import os
from uuid import uuid4
from models.File import File


class StorageService:
    def __init__(self):
        self.dir = current_app.config['STORAGE_DIR']

    def store(self, file:FileStorage):
        if not file:
            return error('error')

        # Prepare file data
        filename = file.filename or ''
        extension = filename.split('.')[-1]
        key = str(uuid4())
        path = self.generate_path(file.mimetype) + key + "." + extension
        size = 0

        try:
            file.save(path)
            size = os.stat(path).st_size
            File.create(filename, key, file.mimetype, size)
        except Exception as e:
            logging.error('Error saving file {}'.format(str(e)))

            return error('error')

        logging.info(filename)
        
        return success('success',{ 'filename': filename, 'key': key, 'size':size })

    def generate_path(self, dir:str):
        current_directory = os.getcwd() + self.dir
        final_directory = os.path.join(current_directory, r"" + dir)

        logging.info(current_directory + dir)

        if not os.path.exists(final_directory):
           os.makedirs(final_directory)

        return current_directory + dir + '/'
