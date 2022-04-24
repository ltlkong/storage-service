from flask import Flask
from dotenv import dotenv_values
import logging
import logging.config
import json
from flask_restful import Api
from models.ConfigType import ConfigType
from resources.AuthResource import LoginResource ,RegisterResource, ApiAuthResource
from resources.TestResource import TestResource

def create_app(config_type: ConfigType): 
    app = Flask(__name__)

    # Environment variables setup
    config = None

    if config_type == ConfigType.DEV:
        config = {
            ** dotenv_values('.env.dev'),
            ** dotenv_values('.env') 
        }

    config = {
        ** dotenv_values('.env.prod'),
        ** dotenv_values('.env') 
    }

    app.config.update(config)

    # Log config
    logger_conf_path = config['LOGGER_CONFIG_PATH']

    if not logger_conf_path:
        raise RuntimeError('Logger config path not specified')
        
    with open(logger_conf_path, 'r') as f:
        logger_conf =json.loads(f.read())

    logging.config.dictConfig(logger_conf)

    return app

def create_api(app: Flask) -> Api:
    api = Api(app)
    init_router(api)

    return api

def init_router(api: Api):
    api.add_resource(LoginResource, '/login')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(ApiAuthResource, '/getkey')
    api.add_resource(TestResource, '/testlogin')
    
