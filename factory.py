from flask import Flask
from dotenv import dotenv_values
import logging
import logging.config
import json
from flask_restful import Api
from resources.AuthResource import LoginResource ,RegisterResource
from resources.ServiceResource import ServiceResource
import os
from resources.StorageResource import StorageResource
from resources.FileResource import FileOperationResource, FileResource

def create_app(config_type): 
    app = Flask(__name__)

    # Environment variables setup
    config = None

    if config_type == 'dev':
        config = {
            ** dotenv_values('.env') ,
        }
    else:
        config = {
            ** dotenv_values('.env.prod')
        }

    app.config.update(config)

    for key in config:
        if config[key] == 'True':
            app.config[key] = True
        if config[key] == 'False':
            app.config[key] = False

    # Log config
    logger_conf_path = config['LOGGER_CONFIG_PATH']

    if not logger_conf_path:
        raise RuntimeError('Logger config path not specified')

    logs_path = os.getcwd() + '/logs/'

    if not os.path.exists(logs_path):
       os.makedirs(logs_path)
        
    with open(logger_conf_path, 'r') as f:
        logger_conf =json.loads(f.read())

    logging.config.dictConfig(logger_conf)

    return app

def create_api(app: Flask) -> Api:
    api = Api(app)
    init_router(api)

    return api

def init_router(api: Api):
    api.add_resource(LoginResource, '/login/<type>')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(ServiceResource, '/service/<service_id>')
    api.add_resource(StorageResource, '/storage')
    api.add_resource(FileResource, '/file')
    api.add_resource(FileOperationResource, '/storage/<storage_id>/file/<file_key>')

    
