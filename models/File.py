from datetime import datetime
from common.core import db, Model
from datetime import datetime
import logging

class File(Model):
    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(300), nullable=False, unique=True)
    type= db.Column(db.String(100), nullable=False)
    size = db.Column(db.BigInteger(), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def create( name, key, type, size):
        file=File(name=name, key=key, type=type, size=size)

        try:
            db.session.add(file)
            db.session.commit()
        except Exception as e:
            logging.error("Error {}".format(str(e)))
            db.session.rollback()

            return False

        logging.info('File {} created'.format(file.name))

        return True
        
        

