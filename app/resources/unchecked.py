from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from datetime import datetime, timezone
from models import Unchecked
import json

class UncheckedController(Resource):
    @jwt_required()
    def get(self):
        # print('current_user', current_user)
        uncheckeds = Unchecked.find().all()

        unchecked_dict = []

        for unchecked in uncheckeds:
            if not unchecked.deleted:
                unchecked_dict.append(unchecked.dict())

        return {'status': 'ok', 'data': unchecked_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            unchecked = Unchecked.get(pk)
            print(unchecked)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        unchecked.deleted = 1
        unchecked.save()

        return {'status': 'ok', 'data': unchecked.dict()}

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
            unchecked = Unchecked.get(pk)
            print(unchecked)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        unchecked.name = args['name']
        unchecked.abbreviation = args['abbreviation']
        unchecked.address = args['address']
        unchecked.day_of_week = args['day_of_week']
        unchecked.start_time = start_time
        unchecked.end_time = end_time
        unchecked.deleted = 0
        unchecked.save()

        return {'status': 'ok', 'data': unchecked.dict()}

    def post(self):
        parser = reqparse.RequestParser()
        print('post>>>>')
        parser.add_argument('first_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('last_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('dob', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('gender', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('wechat', type=str, required=True,
                            help='This field cannot be left blank')

        parser.add_argument('location', type=list[dict], required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('terms', type=list[dict], required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('level', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('email', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('first_emergency_contact', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('second_emergency_contact', type=str, required=True,
                            help='This field cannot be left blank')

        parser.add_argument('find_us', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('referer', type=str, required=True,
                            help='This field cannot be left blank')

        parser.add_argument('message', type=str, required=True,
                            help='This field cannot be left blank')
        # parser.add_argument('checked', type=str, required=True,
        #                     help='This field cannot be left blank')
        # parser.add_argument('verify', type=str, required=True,
        #                     help='This field cannot be left blank')
        parser.add_argument('status', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        print("args", args)

        dob = datetime.strptime(args['dob'], "%Y-%m-%dT%H:%M:%S.%fZ")
        dob = dob.replace(tzinfo=timezone.utc).astimezone(tz=None)

        created = datetime.now()
        created = created.replace(tzinfo=timezone.utc).astimezone(tz=None)

        # handle different level
        ret = []

        # handle different class option
        for class_option in args['location']:
            # print("terms", args['terms'])
            terms = []
            for term in args['terms']:
                terms.append(term['value'])
            print("terms", terms)
            data = {
                'first_name': args['first_name'],
                'last_name': args['last_name'],
                'dob': dob,
                'gender': args['gender'],
                'wechat': args['wechat'],

                'terms': terms,
                'class_option': class_option['class_option_pk'],
                'level': args['level'],
                'email': args['email'],
                'phone': args['phone'],
                'first_emergency_contact': args['first_emergency_contact'],
                'second_emergency_contact': args['second_emergency_contact'],

                'find_us': args['find_us'],
                'referer': args['referer'],

                'message': args['message'],
                'status': args['status'],
                'verify': 0,
                'checked': 0,
                'deleted': 0,
                'created': created,
                'updated': created,
            }
            print("before", data, '\n\n')

            unchecked = Unchecked(**data)
            unchecked.save()
            ret.append(unchecked.dict())

        print("unchecked", ret)

        return {'status': 'ok', 'data': ret}