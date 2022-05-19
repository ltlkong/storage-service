from datetime import datetime
from common.core import db, Model, BasicStatus
from datetime import datetime
from uuid import uuid4

class File(Model):
    __tablename__ = 'file'
    id = db.Column(db.BigInteger(), primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    file_name = db.Column(db.String(300), nullable=False)
    key = db.Column(db.String(300), nullable=False)
    type= db.Column(db.String(100), nullable=False)
    size = db.Column(db.BigInteger(), nullable=False)
    public_key = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(100), nullable=False, default=BasicStatus.ACTIVE)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    storage_id = db.Column(db.BigInteger(), db.ForeignKey('storage.id'), nullable=False)
    storage = db.relationship('Storage',
        backref=db.backref('files', lazy=True))

    previous_file_id=db.Column(db.BigInteger(), db.ForeignKey('file.id'), nullable=True)
    previous_file = db.relationship('File', remote_side=id)

        
    @staticmethod
    def create( file_name, key, type, size, storage_id, previous_file_key, name):
        file=File(file_name=file_name, key=key, type=type, size=size, storage_id=storage_id, public_key=str(uuid4())[:100])

        if name:
            file.name = name
        else:
            file.name = file_name.split('.')[0]

        if previous_file_key:
            previous_file = File.query.filter_by(public_key = previous_file_key, status=BasicStatus.ACTIVE).first()

            if not previous_file:
                raise Exception('Previous version not found')

            previous_file.status =BasicStatus.DISABLED

            file.public_key = previous_file.public_key
            file.previous_file_id = previous_file.id

            if not name:
                file.name = previous_file.name

        try:
            db.session.add(file)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            raise e

        return file

    def json(self, with_internal_key = False):
        file_json = {
            'name': self.name,
            'file_name': self.file_name,
            'public_key': self.public_key,
            'type': self.type,
            'size': self.size,
            'storage_id': self.storage_id,
            'status': self.status
        }

        if with_internal_key:
            file_json['internal_key'] = self.key

        return file_json
