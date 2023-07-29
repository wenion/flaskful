from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

import datetime
from models import Location

class LocationController(Resource):
    @jwt_required()
    def get(self):
        print('current_user', current_user)
        locations = Location.find().all()

        location_dict =[]

        for location in locations:
            location_dict.append(location.dict())

        print("locations", locations)

        return {'status': 'ok', 'data': location_dict}
    
    @jwt_required()
    def delete(self, id):
        pass


    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        parser.add_argument('abbreviation', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        args = parser.parse_args()
        data = {
            'name': args['name'],
            'abbreviation': args['abbreviation']
        }

        location = Location(**data)
        location.save()

        return {'status': 'succ', 'pk': location.pk}