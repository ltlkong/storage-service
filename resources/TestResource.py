from flask.json import jsonify
from flask_restful import Resource, reqparse
from flask import request, current_app
from functools import wraps
from common.core import ApiAuth, Auth

auth = Auth()
api = ApiAuth()

class TestResource(Resource):
    @auth.verify_token
    def get(self):
        return {
            "user":auth.user_id
        }
    @api.verify_api_key
    def post(self):
        return {
            "user":auth.user_id
        }
