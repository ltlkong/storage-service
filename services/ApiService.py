import logging
from uuid import uuid4
from common.responses import error, success
from models.ApiData import ApiData
from common.core import generate_token

class ApiService:
    def generate_api_key(self, user_id, name,enabled_file_types=None):
        if user_id is None:
            logging.error('User id is required to generate_api_key')
            error('Internal error',500)
        if name is None:
            name = str(uuid4())[:50]

        internal_key = str(uuid4())[:150]
        key = generate_token({'user_id':user_id, 'internal_key':internal_key})

        if ApiData.is_name_exist(user_id, name):
            return error('Error name should be unique',400)

        if not ApiData.create(user_id=user_id, api_key=key, enabled_file_types=enabled_file_types, name=name, internal_key=internal_key):
            return error('Error occurred while generating api data',500)

        return success('API data generated', {
                           'key':key,
                           'name': name
                       })

    
    def get_api_data(self, user_id, name=None):
        if name:
            api_data_by_user = map(lambda data: data.dict(), ApiData.get_all(user_id = user_id, name=name))
        else:
            api_data_by_user = map(lambda data: data.dict(), ApiData.get_all(user_id = user_id))

        return success('success', list(api_data_by_user))


