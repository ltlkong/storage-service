import logging
from models.User import User
from common.core import encrypt_md5, generate_token
from flask_restful import abort
from http import HTTPStatus
from datetime import datetime
import re
from operator import and_
from common.core import BasicStatus

class AuthService:
    def register(self, email:str, password:str):
        state = {
            'success':True,
            'http_status': HTTPStatus.CREATED,
            'message' : None,
            'email': email
        }

        if not self.verify_email(email):
            state['message'] = 'Email address is not valid'
            state['http_status'] = HTTPStatus.BAD_REQUEST
            state['success'] = False

        if not self.verify_password(password):
            state['success'] = False
            state['http_status'] = HTTPStatus.BAD_REQUEST
            state['message'] = 'Password is not valid'

        if state['success']:
            try:
                User.create(email=email, password=password)
            except Exception as e:
                state['success'] = False
                state['http_status'] = HTTPStatus.BAD_REQUEST
                state['message'] = str(e)


        if not state['success']:
            logging.error('User registration failed, data: {}'.format(state))
            abort(state['http_status'], message=state['message'])


        state['message'] = 'Registration success'
            
        logging.info('User registered, data: {}'.format(state))

        data = { 'message': state['message']}

        return data

    def loginWithAccount(self, email:str, password:str, remember: bool):
        state = {
            'token_expiry': 1,
            'email': email,
            'password': encrypt_md5(password),
            'success': True,
            'http_status': HTTPStatus.OK,
            'message':None,
            'token' : None,
            'remember_token': None
        }

        user = User.query.filter_by(email=email, password=state['password']).first()

        if not user: 
            state['success'] = False
            state['message'] = 'Email or password incorrect'
            state['http_status'] = HTTPStatus.BAD_REQUEST

        if not state['success']:
            logging.error('User logging failed, data: {}'.format(state))
            abort(state['http_status'], message=state['message'])

        token = generate_token({
            'user_id': user.id
        }, state['token_expiry'])

        state['token'] = token
        user.update(update_login=True, update_remember_token=remember)
        if remember:
            state['remember_token'] = user.get_remember_token()

        logging.info('User logged in, data: {}'.format(state))

        data = {'message': 'Login success', 
            'login': { 
                'token':state['token'],
                'token_expiry': state['token_expiry'],
                'remember_token': state['remember_token']
            }}

        return data

    def loginWithRememberToken(self, remember_token:str):
        state = {
            'token_expiry': 1,
            'remember_token': remember_token,
            'success': True,
            'http_status': HTTPStatus.OK,
            'message':None,
            'token' : None
        }

        user = User.query.filter(and_(User.remember_token == remember_token, User.remember_token_expires_at > datetime.now())).filter_by(status=BasicStatus.ACTIVE).first()

        if not user: 
            state['success'] = False
            state['message'] = 'Invalid token'
            state['http_status'] = HTTPStatus.NOT_FOUND

        if not state['success']:
            logging.error('User logging failed, data: {}'.format(state))
            abort(state['http_status'], message=state['message'])


        token = generate_token({
            'user_id': user.id
        }, state['token_expiry'])

        state['token'] = token
        user.update(update_login=True)
        state = {
            ** state,
            'message' : 'Login success'
        }

        logging.info('User logged in, data: {}'.format(state))

        data = {'message': state['message'], 'login': { 'token':state['token'], 'token_expiry': state['token_expiry'] }}

        return data

    def verify_email(self, email:str) -> bool:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False

        return True
    
    def verify_password(self, password:str) -> bool:
        if len(password) < 8:
            return False

        return True
