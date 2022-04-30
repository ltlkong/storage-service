from flask_restful import Resource, reqparse

class BaseResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()