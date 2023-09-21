from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from datetime import datetime, timezone
from models import Student

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
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        try:
            student = Student.get(pk)
            print(student)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        student.name = args['name']
        student.phone = args['phone']
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
        parser.add_argument('gender', type=str, required=True,
                            help='This field cannot be left blank')
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
        args = parser.parse_args()

        dob = datetime.strptime(args['dob'], "%Y-%m-%dT%H:%M:%S.%fZ")
        dob = dob.replace(tzinfo=timezone.utc).astimezone(tz=None)

        created = datetime.now()
        created = created.replace(tzinfo=timezone.utc).astimezone(tz=None)

        data = {
            'id': len(Student.find().all()) + 1,
            'first_name': args['first_name'],
            'last_name': args['last_name'],
            'dob': dob,
            'gender': args['gender'],
            'wechat': args['wechat'],
            'email': args['email'],
            'phone': args['phone'],
            'first_emergency_contact': args['first_emergency_contact'],
            'second_emergency_contact': args['second_emergency_contact'],
            'referer': args['referer'],
            'created': created,
            'updated': created,
        }

        student = Student(**data)
        student.save()

        return {'status': 'ok', 'data': student.dict()}