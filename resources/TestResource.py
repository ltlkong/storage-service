from flask.json import jsonify
from flask_restful import Resource, reqparse
from flask import request, current_app
from functools import wraps
from common.core import  verify_token

parser = reqparse.RequestParser()

class TestResource(Resource):
    @verify_token
    def get(self, user_id):
        return {
            "user":user_id
        }
