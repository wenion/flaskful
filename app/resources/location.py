from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from datetime import datetime, timezone
from models import Location

class LocationController(Resource):
    @jwt_required()
    def get(self):
        # print('current_user', current_user)
        locations = Location.find().all()

        location_dict =[]

        for location in locations:
            if not location.deleted:
                location_dict.append(location.dict())

        return {'status': 'ok', 'data': location_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            location = Location.get(pk)
            print(location)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

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
        parser.add_argument('address', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('day_of_week', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('start_time', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_time', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        start_time = datetime.strptime(args['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        start_time = start_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

        end_time = datetime.strptime(args['end_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = end_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

        try:
            location = Location.get(pk)
            print(location)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        location.name = args['name']
        location.abbreviation = args['abbreviation']
        location.address = args['address']
        location.day_of_week = args['day_of_week']
        location.start_time = start_time
        location.end_time = end_time
        location.deleted = 0
        location.save()

        return {'status': 'ok', 'data': location.dict()}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('abbreviation', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('address', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('day_of_week', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('start_time', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_time', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        start_time = datetime.strptime(args['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        start_time = start_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

        end_time = datetime.strptime(args['end_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        end_time = end_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
        data = {
            'name': args['name'],
            'abbreviation': args['abbreviation'],
            'address': args['address'],
            'day_of_week': args['day_of_week'],
            'start_time': start_time,
            'end_time': end_time,
        }

        location = Location(**data)
        location.save()

        return {'status': 'ok', 'data': location.dict()}