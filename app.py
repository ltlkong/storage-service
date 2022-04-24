from factory import ConfigType, create_app, create_api
import logging
from flask_cors import CORS
from common.core import db

logger = logging.getLogger(__name__)

app = create_app(ConfigType.DEV)
api = create_api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=app.config['PORT'])
