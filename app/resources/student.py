from flask_restful import Resource, reqparse, abort
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from datetime import datetime, timezone
from models import Student, User
from authenticate import RoleType, Permission

class StudentController(Resource):
    @jwt_required()
    def get(self):
        students = Student.find(Student.deleted == 0).sort_by('id').all()

        student_dict =[]

        for student in students:
            student_dict.append(student.dict())

        return {'status': 'ok', 'data': student_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            student = Student.get(pk)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        student.deleted = 1
        student.save()

        return {'status': 'ok', 'data': student.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('last_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('dob', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('start_date', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('gender', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('wechat', type=str, required=True,
                            help='This field cannot be left blank')
        # parser.add_argument('email', type=str, required=True,
        #                     help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('first_emergency_contact', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('second_emergency_contact', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('referer', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('message', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('memo', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('user_account', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('display', type=int, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        try:
            student = Student.get(pk)
            print(student)
        except NotFoundError:
            return abort(400, message=repr(NotFoundError))

        dob = datetime.strptime(args['dob'], "%Y-%m-%dT%H:%M:%S.%fZ")
        dob = dob.replace(tzinfo=timezone.utc).astimezone(tz=None)

        start_date = datetime.strptime(args['start_date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        start_date = start_date.replace(tzinfo=timezone.utc).astimezone(tz=None)

        student.first_name = args['first_name']
        student.last_name = args['last_name']
        student.dob = dob
        student.start_date = start_date
        student.gender = args['gender']['value']
        student.wechat = args['wechat']
        student.phone = args['phone']
        student.first_emergency_contact = args['first_emergency_contact']
        student.second_emergency_contact = args['second_emergency_contact']
        student.referer = args['referer']
        student.message = args['message']
        student.memo = args['memo']
        student.user_account = args['user_account']['value']
        student.updated = datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None)
        student.display = args['display']
        student.deleted = 0
        student.save()

        return {'status': 'ok', 'data': student.dict()}

    @jwt_required()
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
        parser.add_argument('email', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('first_emergency_contact', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('second_emergency_contact', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('referer', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('message', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('memo', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        dob = datetime.strptime(args['dob'], "%Y-%m-%dT%H:%M:%S.%fZ")
        dob = dob.replace(tzinfo=timezone.utc).astimezone(tz=None)

        created = datetime.now()
        created = created.replace(tzinfo=timezone.utc).astimezone(tz=None)

        exist = Student.find(Student.email == args['email'].lower()).all()
        if len(exist) > 0:
            return abort(400, message='Email has been used')

        print("hrer11", student)
        data = {
            'id': len(Student.find().all()) + 1,
            'first_name': args['first_name'],
            'last_name': args['last_name'],
            'dob': dob,
            'start_date': created,
            'gender': args['gender']['value'],
            'wechat': args['wechat'],
            'email': args['email'].lower(),
            'phone': args['phone'],
            'first_emergency_contact': args['first_emergency_contact'],
            'second_emergency_contact': args['second_emergency_contact'],
            'referer': args['referer'],
            'message': args['message'],
            'memo': args['memo'],
            'role_type': RoleType.STUDENT,
            'lessons': [],
            'user_account': '',
            'created': created,
            'updated': created,
        }

        student = Student(**data)

        user_data = {
            'id': len(User.find().all()) + 1,
            'account_name': args['first_name'],
            'email': args['email'].lower(),
            'phone': args['phone'],
            'password': User.hash_password(args['first_name']),
            'auth': Permission.MINIMUM,
            'role_type': RoleType.STUDENT,
            'binding_account': student.pk,
            'created': created,
            'updated': created,
        }

        exist = User.find(User.email == args['email'].lower()).all()
        if len(exist) == 0:
            user = User(**user_data)
            user.save()
        else:
            user = exist[0]

        student.user_account = user.pk
        student.save()

        return {'status': 'ok', 'data': student.dict()}