import logging 
from common.response import Response 
from flask_restful import abort
from http import HTTPStatus
from models.User import User
from models.Service import Service
from models.Storage import Storage

class StorageService:
    def create(self, service, name, type, enabled_file_types):
        state = {
            'http_status': HTTPStatus.CREATED,
            'success': True,
            'message': 'Storage created',
        }

        storage = None

        try:
            storage = Storage.create(service=service, name=name, type=type, enabled_file_types=enabled_file_types)
        except Exception as e:
            state['http_status'] = HTTPStatus.BAD_REQUEST
            state['success'] = False
            state['message'] = str(e)

        if not state['success']:
            logging.error('Error creating service, data:{}'.format(state))
            abort(state['http_status'], message=state['message'])

        logging.info('Service created, data:{}'.format(state))

        data = { 'message': state['message'], 'storage':  storage.json() if storage else None }

        return data
    def get(self, service, name = None, type = None):
        storages = Storage.query.filter_by(service_id = service.id)

        if name:
            storages = storages.filter_by(name = name)
        if type:
            storages = storages.filter_by(type = type)

        data = { "message": "Storages", "storages": list(map(lambda s: s.json(), storages)) }

        return data

    # TODO: update
    def update(self, user, name):
        return { 'message': 'updated'}

    # TODO: deactive
    def deactive(self, user, storage_id):
        return { 'message': 'delete'}
