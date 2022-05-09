from datetime import datetime, timedelta
from common.core import Model, db, encrypt_md5
from datetime import datetime, timedelta
from uuid import uuid4

class UserStatus:
    ACTIVE = 'active'
    DEACTIVE = 'deactive'
    BANNED = 'banned'

class User(Model):
    __tablename__='user'
    id = db.Column(db.String(100), primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    status= db.Column(db.String(50), nullable=False, default=UserStatus.ACTIVE)
    service_limit = db.Column(db.Integer, nullable=False, default=3)

    remember_token = db.Column(db.String(100), nullable=True)
    remember_token_expires_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_login_at = db.Column(db.DateTime, nullable=True, default=datetime.now())

    def set_remember_token(self):
        self.remember_token=str(uuid4())[:100]
        self.remember_token_expires_at = datetime.now() + timedelta(days = 7)
    def get_remember_token(self):
        if self.remember_token_expires_at and self.remember_token_expires_at < datetime.now():
            return None
        return self.remember_token

    @staticmethod
    def create(email:str, password:str):
        if User.query.filter_by(email=email).first():
            raise Exception("User already exists")

        hash_password = encrypt_md5(password)

        user=User(id=str(uuid4())[:100],email=email, password=hash_password)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            raise e

        return user

    def update(self, email=None, password=None, update_login=False, update_remember_token = False):
        if email:
            self.email=email
        if password:
            self.password = encrypt_md5(password)
        if update_login:
            self.last_login_at = datetime.now()
        if update_remember_token:
            self.set_remember_token()

        self.updated_at=datetime.now()

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

            raise e

        return True
