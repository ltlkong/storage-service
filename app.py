from factory import  create_app, create_api
import logging
from flask_cors import CORS
from common.core import db
import os
import waitress

logger = logging.getLogger(__name__)

app = create_app(os.environ.get('ENVIRONMENT'))
api = create_api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    logging.info("Starting server")
    if app.config['ENVIRONMENT'] == 'dev':
        app.run(host='0.0.0.0',port=app.config['PORT'])
    waitress.serve(app,host='0.0.0.0',port=app.config['PORT'], max_request_body_size=10000000000,threads=6)
