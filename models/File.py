from datetime import datetime
from common.core import db, Model
from datetime import datetime
import logging

class File(Model):
    __tablename__ = 'files'
    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(300), nullable=False, unique=True)
    type= db.Column(db.String(100), nullable=False)
    size = db.Column(db.BigInteger(), nullable=False)
    previous_version=db.Column(db.BigInteger(), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    api_data_key = db.Column(db.String(500), db.ForeignKey('api_data.internal_key'), nullable=False)
    api_data = db.relationship('ApiData',
        backref=db.backref('files', lazy=True))

    @staticmethod
    def get(**kwargs):
        files = db.session.query(File).filter_by(**kwargs)

        return files

    @staticmethod
    def filter(**kwargs):
        files = db.session.query(File).filter(**kwargs)

        return files

        
    @staticmethod
    def create( name, key, type, size, api_data_key):
        file=File(name=name, key=key, type=type, size=size, api_data_key=api_data_key)

        try:
            db.session.add(file)
            db.session.commit()
        except Exception as e:
            logging.error("Error {}".format(str(e)))
            db.session.rollback()

            return False

        logging.info('File {} created'.format(file.name))

        return True

    def dict(self):
        return {
            'name': self.name,
            'key': self.key,
            'type': self.type

        }
