from datetime import datetime
from common.core import db, Model
from datetime import datetime

class File(Model):
    __tablename__ = 'file'
    id = db.Column(db.BigInteger(), primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(300), nullable=False, unique=True)
    type= db.Column(db.String(100), nullable=False)
    size = db.Column(db.BigInteger(), nullable=False)
    previous_version=db.Column(db.String(300), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    storage_id = db.Column(db.BigInteger(), db.ForeignKey('storage.id'), nullable=False)
    storage = db.relationship('Storage',
        backref=db.backref('file', lazy=True))


        
    @staticmethod
    def create( name, key, type, size, storage_id, previous_file_key = None):
        file=File(name=name, key=key, type=type, size=size, storage_id=storage_id)

        if previous_file_key:
            file.previous_version = previous_file_key

        try:
            db.session.add(file)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            raise e

        return file

    def json(self):
        return {
            'name': self.name,
            'key': self.key,
            'type': self.type,
            'size': self.size,
            'storage_id': self.storage_id,
            'url': '/storage/{}/file/{}'.format(self.storage_id, self.key),
            'previous_file_key': self.previous_file_key
        }
