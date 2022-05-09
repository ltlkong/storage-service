from datetime import datetime
from common.core import Model, db, encrypt_md5
from datetime import datetime
from uuid import uuid4

class Service(Model):
    __tablename__='service'
    id = db.Column(db.BigInteger(), primary_key=True)
    key = db.Column(db.String(200), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('services', lazy=True))


    @staticmethod
    def create(name,user, description=None):
        user_services = Service.query.filter_by(user_id=user.id)

        if (user_services.count() >= user.service_limit):
            raise Exception('Service limit exceeded')
        if (user_services.filter_by(name=name).count() != 0):
            raise Exception('Service name already exists')

        service = Service(key=str(uuid4())[:200], name= name or 's' + str(user_services.count() + 1), description= description, user_id=user.id)

        try: 
            db.session.add(service)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            raise e

        return service

    def json(self):
        return { 'key': self.key, 'name': self.name, 'description': self.description}
