from http import HTTPStatus

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
