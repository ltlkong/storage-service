import logging
from uuid import uuid4
from common.responses import  success
from models.Storage import Storage
from common.core import generate_token
from utils.clear_none_in_dict import clear_none_in_dict
from flask_restful import abort
from http import HTTPStatus

class ApiService:
    def generate_api_key(self, user_id, name=None,enabled_file_types=None):
        if Storage.is_name_exist(user_id, name):
            abort(HTTPStatus.BAD_REQUEST, message='Name already exist')

        # Generate token
        internal_key = str(uuid4())[:150]
        key = generate_token({'user_id':user_id, 'internal_key':internal_key})


        if not Storage.create(user_id=user_id, api_key=key, enabled_file_types=enabled_file_types, name=name, internal_key=internal_key):
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message='Error creating storage')

        logging.info("Api key {} created".format(name))

        return success('API key generated', {
                           'key':key,
                           'name': name
                       })

    def get_storage_key(self, user_id, **kwargs):
        new_kwargs = clear_none_in_dict(**kwargs)

        key_by_user = map(lambda data: data.dict(), Storage.filter(user_id = user_id, **new_kwargs))

        return success('Avaliable API data', list(key_by_user))