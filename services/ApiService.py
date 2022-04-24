import logging
from uuid import uuid4

from flask_restful import fields, marshal, marshal_with
from common.responses import error, success
from models.ApiData import ApiData
from common.core import generate_token
import json

class ApiService:
    def generate_api_key(self, user_id, enabled_file_types=None):
        if user_id is None:
            logging.error('User id is required to generate_api_key')
            error('Internal error',500)

        key = generate_token({'user_id':user_id, 'random': str(uuid4())[:50]})

        if not ApiData.create(user_id=user_id, api_key=key, enabled_file_types=enabled_file_types):
            return error('Error occurred while generating api data',500)

        return success('API data generated', {
                           'key':key,
                           'enabled_file_types':enabled_file_types
                       })

    
    def get_api_data(self, user_id):
        api_data_by_user = list(map(lambda data: data.dict(), ApiData.get_all(user_id = user_id)))

        return success('success', api_data_by_user)



