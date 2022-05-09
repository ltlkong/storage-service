import logging
from flask_restful import abort
from http import HTTPStatus
from models.Service import Service

class ApiService:
    def create_service(self, user, name, description=None):
        state = {
            'http_status': HTTPStatus.CREATED,
            'success': True,
            'message': 'Service created',
            'service_key': None
        }

        service = None

        try:
            service = Service.create(name=name, description=description, user=user)
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

    def get_services(self, user, name=None):
        services = Service.query.filter_by(user_id=user.id)

        if name:
            services = services.filter_by(name=name)

        return list(map(lambda s: s.json(), services))
