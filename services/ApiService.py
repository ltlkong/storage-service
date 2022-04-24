import logging
from uuid import uuid4
from common.responses import error, success
from models.ApiData import ApiData
from common.core import generate_token
from utils.clear_none_in_dict import clear_none_in_dict

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

    
    def get_api_data(self, user_id, **kwargs):
        new_kwargs = clear_none_in_dict(**kwargs)

        api_data_by_user = map(lambda data: data.dict(), ApiData.get_all(user_id = user_id, **new_kwargs))

        return success('Avaliable API data', list(api_data_by_user))


