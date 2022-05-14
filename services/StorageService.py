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
        storages = Storage.query.filter_by(service_id = service.id, status='active')

        if name:
            storages = storages.filter_by(name = name)
        if type:
            storages = storages.filter_by(type = type)

        data = { "message": "Storages", "storages": list(map(lambda s: s.json(), storages)) }

        return data

    def update(self, service, storage_id, name):
        state = {
            'http_status': HTTPStatus.OK,
            'success': True,
            'message': 'Service updated',
            'service_id': None
        }

        storage = Storage.query.filter_by(id=storage_id, service_id=service.id).first()

        if storage is None:
            state['success'] = False
            state['http_status'] = HTTPStatus.NOT_FOUND
            state['message'] = 'Service not found'
        if not storage.update(name):
            state['success'] = False
            state['http_status'] = HTTPStatus.INTERNAL_SERVER_ERROR

        if not state['success']:
            logging.error('Error updating service, data:{}'.format(state))
            abort(state['http_status'], message=state['message'])

        return {'message': 'Updated' }

    def deactive(self, service, storage_id):
        state = {
            'http_status': HTTPStatus.OK,
            'success': True,
            'message': 'Service updated',
            'service_id': None
        }

        storage = Storage.query.filter_by(id=storage_id, service_id=service.id).first()

        if storage is None:
            state['success'] = False
            state['http_status'] = HTTPStatus.NOT_FOUND
            state['message'] = 'Service not found'
        if not storage.update(status='deactive'):
            state['success'] = False
            state['http_status'] = HTTPStatus.INTERNAL_SERVER_ERROR

        if not state['success']:
            logging.error('Error updating service, data:{}'.format(state))
            abort(state['http_status'], message=state['message'])

        return {'message': 'Deleted' }
