import logging
from os import stat
from flask_restful import abort
from http import HTTPStatus
from models.Service import Service

class ApiService:
    def set_user(self,user):
        self.user = user

    def create(self, name, description=None):
        state = {
            'http_status': HTTPStatus.CREATED,
            'success': True,
            'message': 'Service created',
            'service_id': None
        }

        service = None

        try:
            service = Service.create(name=name, description=description, user=self.user)
            state['service_id'] = service.id
        except Exception as e:
            state['http_status'] = HTTPStatus.BAD_REQUEST
            state['success'] = False
            state['message'] = str(e)

            
        if not state['success']:
            logging.error('Error creating service, data:{}'.format(state))
            abort(state['http_status'], message=state['message'])

        logging.info('Service created, data:{}'.format(state))

        data = { 'message': state['message'], 'service':  service.json() if service else None }

        return data

    def get(self, name=None):
        services = Service.query.filter_by(user_id=self.user.id)

        if name:
            services = services.filter_by(name=name)

        return list(map(lambda s: s.json(), services))

    def update(self,key, name, description):
        state = {
            'http_status': HTTPStatus.OK,
            'success': True,
            'message': 'Service updated',
            'service_id': None
        }

        service = Service.query.filter_by(key=key, user_id=self.user.id).first()

        state['service_id'] = service.id

        if service is None:
            state['success'] = False
            state['http_status'] = HTTPStatus.NOT_FOUND
            state['message'] = 'Service not found'
        if not service.update(name, description):
            state['success'] = False
            state['http_status'] = HTTPStatus.INTERNAL_SERVER_ERROR

        if not state['success']:
            logging.error('Error updating service, data:{}'.format(state))
            abort(state['http_status'], message=state['message'])

        return {'message': 'Updated' }
