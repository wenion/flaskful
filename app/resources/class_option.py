from flask_restful import Resource, reqparse, inputs
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from typing import Optional, List

from dateutil import parser as date_parser
from dateutil.tz import tzutc
import pytz
from models import ClassOption

class ClassOptionController(Resource):
    # @jwt_required()
    def get(self):
        class_options = ClassOption.find(ClassOption.deleted == 0).sort_by('id').all()

        class_option_dict =[]

        for class_option in class_options:
            # if not class_option.deleted:
            class_option_dict.append(class_option.dict())
        # print("class_option", class_option_dict)

        return {'status': 'ok', 'data': class_option_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            class_option = ClassOption.get(pk)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        class_option.deleted = 1
        class_option.save()

        return {'status': 'ok', 'data': class_option.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('class_code', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('location', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('day_of_week', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('level', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('start_time', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_time', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('year', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('memeo', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('display', type=int, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        # print("put args", args['day_of_week'])
        try:
            class_option = ClassOption.get(pk)
            # print(class_option)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        start_time = date_parser.parse(args['start_time'])
        end_time = date_parser.parse(args['end_time'])
        # term_args = args['terms']
        # term_list = [term['value'] for term in term_args if 'value' in term]

        class_option.class_code = args['class_code']
        class_option.location = args['location']['value']
        class_option.day_of_week = args['day_of_week']['value']
        class_option.level = args['level']['value']
        class_option.start_time = start_time
        class_option.end_time = end_time
        class_option.year = args['year']
        class_option.memeo = args['memeo']
        class_option.display = args['display']
        # class_option.deleted = 0
        class_option.save()

        return {'status': 'ok', 'data': class_option.dict()}

    @jwt_required()
    def post(self):        
        parser = reqparse.RequestParser()
        parser.add_argument('class_code', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('location', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('day_of_week', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('start_time', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_time', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('level', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('year', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('memeo', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        start_time = date_parser.parse(args['start_time'])
        end_time = date_parser.parse(args['end_time'])
        # term_args = args['terms']
        # term_list = [term['value'] for term in term_args if 'value' in term]
        # print("data args", args)

        data = {
            'id': len(ClassOption.find().all()) + 1,
            'class_code': args['class_code'],
            'location': args['location']['value'],
            'level': args['level']['value'],
            'day_of_week': args['day_of_week']['value'],
            'start_time': start_time,
            'end_time': end_time,
            'year': args['year'],
            'memeo': args['memeo'],
        }

        class_option = ClassOption(**data)
        class_option.save()

        return {'status': 'ok', 'data': class_option.dict()}