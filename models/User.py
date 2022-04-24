from datetime import datetime
from common.core import Model, db, encrypt_md5
from datetime import datetime
from uuid import uuid4
import logging

class User(Model):
    id = db.Column(db.String(100), primary_key=True)
# first_name = db.Column(db.String(100), nullable=False)
# last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(150), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def get(**kwargs):
        user = db.session.query(User).filter_by(**kwargs).first()

        return  user

    @staticmethod
    def create(email:str, password:str):
        hash_password = encrypt_md5(password)

        user=User(id=str(uuid4())[:100],email=email, password=hash_password)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            logging.error("Error {}".format(str(e)))
            db.session.rollback()

            return False

        logging.info('User {} registration successful'.format(user.email))

        return True

    def update(self, api_key=None, email=None, password=None):
        if api_key:
            self.api_key=api_key
        if email:
            self.email=email
        if password:
            self.password = encrypt_md5(password)

        self.updated_at=datetime.now()

        try:
            db.session.commit()

            return True
        except Exception as e:
            logging.error("Error {}".format(str(e)))

        return False

        

