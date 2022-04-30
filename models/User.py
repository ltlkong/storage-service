from datetime import datetime
from enum import Enum
from common.core import Model, db, encrypt_md5
from datetime import datetime
from uuid import uuid4
import logging

class UserStatus:
    ACTIVE = 'active'
    DEACTIVE = 'deactive'
    BANNED = 'banned'


class User(Model):
    __tablename__='users'
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    status= db.Column(db.String(50), nullable=False, default=UserStatus.ACTIVE)
    # TODO: Allowed number of api data

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_login_at = db.Column(db.DateTime, nullable=True, default=datetime.now)

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

        logging.info('User {} registered'.format(user.email))

        return True

    def update(self,  email=None, password=None, update_login=False):
        if email:
            self.email=email
        if password:
            self.password = encrypt_md5(password)
        if update_login:
            self.last_login_at = datetime.now()

        self.updated_at=datetime.now()

        try:
            db.session.commit()

            logging.info("User {} updated".format(self.email))

            return True
        except Exception as e:
            logging.error("Error {}".format(str(e)))

        return False

        

