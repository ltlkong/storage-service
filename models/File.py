from datetime import datetime
from common.core import db, Model
from datetime import datetime

class File(Model):
    __tablename__ = 'file'
    id = db.Column(db.BigInteger(), primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    file_name = db.Column(db.String(300), nullable=False)
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
    def create( file_name, key, type, size, storage_id, previous_file_key, name):
        file=File(file_name=file_name, key=key, type=type, size=size, storage_id=storage_id)

        if previous_file_key:
            previous_file = File.query.filter_by(previous_version = previous_file_key).first()

            if not previous_file:
                raise Exception('Previous version not found')

            file.previous_version = previous_file.json()['url']
        if name:
            file.name = name
        else:
            file.name = file_name.split('.')[0]

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
            'file_name': self.file_name,
            'key': self.key,
            'type': self.type,
            'size': self.size,
            'storage_id': self.storage_id,
            'url': '/storage/{}/file/{}'.format(self.storage_id, self.key),
            'previous_version_url': self.previous_version
        }
