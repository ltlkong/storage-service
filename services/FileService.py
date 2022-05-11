from werkzeug.datastructures import FileStorage
import logging
from flask import current_app
import os
from uuid import uuid4
from models.File import File
from models.Storage import Storage
from flask_restful import abort
from http import HTTPStatus

# Abstract
class FileService:
    def upload(self, file:FileStorage, previous_file_key= None) :
        pass

    def download(self, file_key):
        pass

    def get(self, name=None, type=None, key=None):
        pass

# Factory
def create_file_service(storage_id, service=None):
    storage = Storage.query.filter_by(id = storage_id)

    if service:
        storage =  storage.filter_by(service_id = service.id)

    storage = storage.first()

    if storage is None:
        abort(HTTPStatus.NOT_FOUND, message="Storage not found")

    return LocalFileService(storage)

# Store files in server
class LocalFileService(FileService):
    def __init__(self, storage):
        self.dir = current_app.config['STORAGE_DIR']
        self.storage = storage

    # Store a file to the storage dir
    def upload(self, file:FileStorage, previous_file_key = None):
        state = {
            'http_status': HTTPStatus.CREATED,
            'success': True,
            'message': 'File uploaded',
            'filename':None,
            'size': None,
            'key': None,
            'type': None,
            'path': None,
            'file_type': None
        }

        # Check if file types supported
        state['file_type'] = file.mimetype.split('/')[0]

        if self.storage.get_enabled_file_types() and state['file_type'] not in self.storage.get_enabled_file_types():
            state['http_status'] = HTTPStatus.BAD_REQUEST
            state['success'] = False
            state['message'] = 'File type not supported: {}'.format(state['file_type'])
            
        if not state['success']:
            logging.error('Error saving file {}'.format(state))
            abort(400, message=state['message'])

        # Prepare file data
        state['filename'] = file.filename or 'unknown'
        state['key'] = str(uuid4()) 
        state['path'] = self.generate_path(state['file_type']) + state['key'] +'.' + state['filename'].split('.')[-1]

        try:
            file.save(state['path'])
            state['size'] = os.stat(state['path']).st_size
            File.create(state['filename'], state['key'], state['file_type'], state['size'], self.storage.id,previous_file_key)
        except Exception as e:
            state['http_status'] = HTTPStatus.INTERNAL_SERVER_ERROR
            state['success'] = False
            state['message'] = 'Error saving file to server: {}'.format(str(e))

        if not state['success']:
            logging.error('Error saving file, data: {}'.format(state))
            abort(500, message=state['message'])

        logging.info('File saved, data: {}'.format(state))

        data = {'message': state['message'],  'file': { 'filename': state['filename'], 'key': state['key'], 'size':state['size'], 'type': state['file_type'] }}
        
        return data

    # Get all files object from current api key
    def get(self, name, type, key):
        files = File.query.filter_by(storage_id = self.storage.id)

        if name:
            files = files.filter_by(name=name)
        if type:
            files = files.filter_by(type=type)
        if key:
            files = files.filter_by(key=key)

        files_json = list(map(lambda f: f.json(), files))

        data = { 'message': 'Files', 'files': files_json}

        return data

    def download(self, key):
        file = File.query.filter_by(key=key).first()

        if file is None:
            abort(404, message='File not found')

        data = {'path':self.generate_path(file.type) + key +'.' + file.name.split('.')[-1]}

        return data
        

    def generate_path(self, dir:str):
        current_directory = os.getcwd() + self.dir
        final_directory = os.path.join(current_directory, r"" + dir)

        if not os.path.exists(final_directory):
           os.makedirs(final_directory)

        return current_directory + dir + '/'

    def is_file_type_supported(self, file_type, allowed_file_types):
        return file_type in allowed_file_types

