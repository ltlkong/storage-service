from datetime import datetime
from common.core import db, Model
from datetime import datetime
import logging

class File(Model):
    __tablename__ = 'file'
    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(300), nullable=False, unique=True)
    type= db.Column(db.String(100), nullable=False)
    size = db.Column(db.BigInteger(), nullable=False)
    previous_version=db.Column(db.BigInteger(), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    storage_id = db.Column(db.BigInteger(), db.ForeignKey('storage.id'), nullable=False)
    storage = db.relationship('Storage',
        backref=db.backref('file', lazy=True))

    @staticmethod
    def get(**kwargs):
        files = File.filter(**kwargs).first()

        return files

    @staticmethod
    def filter(**kwargs):
        files = db.session.query(File).filter_by(**kwargs)

        return files

        
    @staticmethod
    def create( name, key, type, size, storage_key):
        file=File(name=name, key=key, type=type, size=size, storage_key=storage_key)

        try:
            db.session.add(file)
            db.session.commit()
        except Exception as e:
            logging.error("Error {}".format(str(e)))
            db.session.rollback()

            return False

        return True

    def dict(self):
        return {
            'name': self.name,
            'key': self.key,
            'type': self.type
        }
