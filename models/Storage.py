from datetime import datetime
from common.core import Model, db
from datetime import datetime
import logging
from uuid import uuid4

class ApiStatus: 
    ACTIVE ='active'
    DEACTIVE = 'deactive'

class Storage(Model):
    __tablename__ = 'storage'
    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    internal_key = db.Column(db.String(150), nullable=False, unique=True)
    enabled_file_types = db.Column(db.Text, nullable=True)
    api_key=db.Column(db.String(500), nullable=False,unique=True)
    status=db.Column(db.String(50), nullable=False, default=ApiStatus.ACTIVE)

    # Storage size

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User',
        backref=db.backref('storage', lazy=True))

    def get_enabled_file_types(self):
        if not self.enabled_file_types :
            return None
        return self.enabled_file_types.split(',')

    def set_enabled_file_types(self, enabled_file_types):
        self.enabled_file_types = ','.join(enabled_file_types)
        
    @staticmethod
    def get(**kwargs):
        storage = db.session.query(Storage).filter_by(**kwargs).first()

        return  storage

    @staticmethod
    def get_all(**kwargs):
        storage_by = db.session.query(Storage).filter_by(**kwargs)

        return  storage_by

    @staticmethod
    def create(user_id,api_key,name, internal_key:str, enabled_file_types=None):
        storage=Storage(user_id=user_id, api_key=api_key, name=name, internal_key = internal_key)
        if enabled_file_types:
            storage.set_enabled_file_types(enabled_file_types)

        try:
            db.session.add(storage)
            db.session.commit()
        except Exception as e:
            logging.error("Error {}".format(str(e)))

            db.session.rollback()

            return False

        logging.info('Api data {} geneared'.format(storage.id))

        return True
    @staticmethod
    def is_name_exist(user_id, name):
        try:
            return len(list(map(lambda data: data.name,Storage.get_all(user_id=user_id, name=name)))) > 0
        except Exception as e:
            logging.error("Error {}".format(str(e)))

            return False

    def update(self, api_key=None, user_id=None, name=None):
        if api_key:
            self.api_key = api_key
        if name:
            self.name = name
        if user_id:
            self.user_id = user_id

        self.updated_at=datetime.now()

        try:
            db.session.commit()

            logging.info("Api data {} updated".format(self.email))

            return True
        except Exception as e:
            logging.error("Error {}".format(str(e)))

        return False

    def dict(self):
        data = {
            'api_key': self.api_key,
            'enabled_file_types': self.get_enabled_file_types(),
            'name': self.name,
            'status':self.status
        }

        return data
