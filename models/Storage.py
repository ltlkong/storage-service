from datetime import datetime
from common.core import Model, db
from datetime import datetime

from models.Service import Service
import logging

class StorageType:
    AMAZONS3 = 'amazon s3'
    SERVER = 'server'
    GOOGLECLOUD = 'google cloud'

    types = { AMAZONS3, SERVER, GOOGLECLOUD}

class FileType:
    IMAGE = 'image'
    AUDIO = 'audio'
    TEXT = 'text'
    VIDEO = 'video'
    APPLICATION = 'application'

    types = { IMAGE, AUDIO, TEXT, VIDEO, APPLICATION}

class Storage(Model):
    __tablename__ = 'storage'
    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    enabled_file_types = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=False, default=StorageType.SERVER)
    status=db.Column(db.String(50), nullable=False, default='active')
    third_party_key = db.Column(db.String(800), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    service_id = db.Column(db.BigInteger(), db.ForeignKey('service.id'), nullable=True)
    service = db.relationship('Service', backref=db.backref('storages', lazy=True))

    # Allowed file types
    def get_enabled_file_types(self):
        if not self.enabled_file_types :
            return None
        return self.enabled_file_types.split(',')

    def set_enabled_file_types(self, enabled_file_types):
        file_types = list(map(lambda t: t.split('/')[0], enabled_file_types))

        # Check if all types are supported
        for t in file_types:
            if t not in FileType.types:
                raise Exception('Enabled file types contain unsupported type')

        self.enabled_file_types = ','.join(file_types)

    @staticmethod
    def create(service:Service, name:None, type=None, enabled_file_types=None, third_party_key=None):
        storage = Storage(service_id = service.id)
        storage.name = 'storage ' + str(len(service.storages) + 1)

        if name:
            storage.name = name

        if Storage.query.filter_by(name=name, service_id=service.id).count() > 0:
            raise Exception('Storage name must be unique')

        if type and type in StorageType.types:
            storage.type = type
        else:
            raise Exception('Storage type one of {}'.format(StorageType.types))
        
        if storage.type != StorageType.SERVER and third_party_key is None:
            raise Exception(storage.type + " key can't be None")
            
        if enabled_file_types:
            storage.set_enabled_file_types(enabled_file_types)

        try:
            db.session.add(storage)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            raise e

        return storage

    def update(self, service_id=None, name=None):
        if name:
            self.name = name
        if service_id:
            self.service_id = service_id

        self.updated_at=datetime.now()

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        return True

    def json(self):
        return {
            'enabled_file_types': self.get_enabled_file_types(),
            'name': self.name,
            'status':self.status,
            'type': self.type
        }
