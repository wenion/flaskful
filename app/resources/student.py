from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

import datetime
from models import Student

class StudentController(Resource):
    @jwt_required()
    def get(self):
        students = Student.find().all()

        student_dict =[]

        for student in students:
            print(student)
            if not student.deleted:
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
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        data = {
            'name': args['name'],
            'phone': args['phone'],
            'class_list': []
        }

        student = Student(**data)
        student.save()

        return {'status': 'ok', 'data': student.dict()}