from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from datetime import datetime, timezone
from app.models import Unchecked, Lesson, Student
import json

class UncheckedController(Resource):
    @jwt_required()
    def get(self):
        # print('current_user', current_user)
        uncheckeds = Unchecked.find(Unchecked.deleted == 0).sort_by('id').all()

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
        print("print put")
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('last_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('dob', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('gender', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('wechat', type=str, required=True,
                            help='This field cannot be left blank')

        parser.add_argument('email', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('first_emergency_contact', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('second_emergency_contact', type=str, required=True,
                            help='This field cannot be left blank')
                            
        parser.add_argument('student', type=dict, location='json')

        parser.add_argument('referer', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('message', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('memo', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('checked', type=int, required=True,
                            help='This field cannot be left blank')

        
        parser.add_argument('class_option', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('verify', type=int, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('status', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('trial', type=int)
        parser.add_argument('terms', type=list[dict], location='json')
       
        args = parser.parse_args()
        verify = args['verify'] and args['terms']


        dob = datetime.strptime(args['dob'], "%Y-%m-%dT%H:%M:%S.%fZ")
        dob = dob.replace(tzinfo=timezone.utc).astimezone(tz=None)

        # start_time = datetime.strptime(args['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # start_time = start_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

        # end_time = datetime.strptime(args['end_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # end_time = end_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

        try:
            unchecked = Unchecked.get(pk)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        unchecked.first_name = args['first_name']
        unchecked.last_name = args['last_name']
        unchecked.dob = dob
        unchecked.gender = args['gender']['value']
        unchecked.wechat = args['wechat']

        # unchecked.term = args['term']
        # unchecked.level = args['level']
        # unchecked.email = args['email']
        unchecked.phone = args['phone']
        unchecked.first_emergency_contact = args['first_emergency_contact']
        unchecked.second_emergency_contact = args['second_emergency_contact']

        unchecked.referer = args['referer']
        unchecked.message = args['message']
        unchecked.memo = args['memo']
        unchecked.checked = args['checked']

        unchecked.class_option = args['class_option']['value']
        unchecked.verify = args['verify']
        unchecked.trial = args['trial']

        if verify:
            for group in args['terms']:
                if group:
                    for plan_lesson in group:
                        try:
                            lesson = Lesson.get(plan_lesson['pk'])
                        except NotFoundError:
                            pass
                        else:
                            if args['student']['pk'] not in lesson.students:
                                lesson.students.append(args['student']['pk'])
                                lesson.save()
                        try:
                            student = Student.get(args['student']['pk'])
                        except NotFoundError:
                            pass
                        else:
                            if plan_lesson['pk'] not in student.lessons:
                                student.lessons.append(plan_lesson['pk'])
                                student.save()


        # unchecked.status = args['status']
        # unchecked.student = args['student']
        # unchecked.plan_lesson = args['plan_lesson']
        unchecked.updated = datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None)
        unchecked.deleted = 0
        unchecked.save()

        return {'status': 'ok', 'data': unchecked.dict()}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('last_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('dob', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('gender', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('wechat', type=str, required=True,
                            help='This field cannot be left blank')

        parser.add_argument('level', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('class_option', type=list[dict], required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('term', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
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

        dob = datetime.strptime(args['dob'], "%Y-%m-%dT%H:%M:%S.%fZ")
        dob = dob.replace(tzinfo=timezone.utc).astimezone(tz=None)

        created = datetime.now()
        created = created.replace(tzinfo=timezone.utc).astimezone(tz=None)

        # handle different level
        ret = []

        # handle different class option
        for class_option in args['class_option']:
            data = {
                'id': len(Unchecked.find().all()) + 1,
                'first_name': args['first_name'],
                'last_name': args['last_name'],
                'dob': dob,
                'gender': args['gender']['value'],
                'wechat': args['wechat'],

                'term': args['term']['value'],
                'class_option': class_option['value'],
                'level': args['level'],
                'email': args['email'].lower(),
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
                'student': '',
                'plan_lesson': '',
                'memo': '',
                'created': created,
                'updated': created,
            }

            unchecked = Unchecked(**data)
            unchecked.save()
            ret.append(unchecked.dict())

        return {'status': 'ok', 'data': ret}