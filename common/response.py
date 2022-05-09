from http import HTTPStatus
from flask import current_app, send_file

class Response:
    @staticmethod
    def ok(message= 'Success', data = None):
        if data:
            return {
                'message':message,
                'data':data
            }, HTTPStatus.OK

        return {
            'message':message,
        }, HTTPStatus.OK
    
    @staticmethod
    def created(message= 'Created', data = None):
        if data:
            return {
                'message':message,
                'data':data
            }, HTTPStatus.CREATED

        return {
            'message':message,
        }, HTTPStatus.CREATED

    @staticmethod
    def file(path_or_file):
        return send_file(path_or_file=path_or_file)
