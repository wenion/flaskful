from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

import datetime
from models import Location

class LocationController(Resource):
    @jwt_required()
    def get(self):
        # print('current_user', current_user)
        locations = Location.find().all()

        location_dict =[]

        for location in locations:
            location_dict.append(location.dict())

        return {'status': 'ok', 'data': location_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            location = Location.get(pk)
            print(location)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        location.deleted = 1
        location.save()

        return {'status': 'ok', 'data': location.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('abbreviation', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        try:
            location = Location.get(pk)
            print(location)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        location.name = args['name']
        location.abbreviation = args['abbreviation']
        location.save()

        return {'status': 'ok', 'data': location.dict()}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('abbreviation', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        data = {
            'name': args['name'],
            'abbreviation': args['abbreviation']
        }

        location = Location(**data)
        location.save()

        return {'status': 'ok', 'data': location.dict()}