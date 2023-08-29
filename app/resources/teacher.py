from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

import datetime
from models import Teacher

class TeacherController(Resource):
    @jwt_required()
    def get(self):
        teachers = Teacher.find().all()

        teacher_dict =[]

        for teacher in teachers:
            print(teacher)
            if not teacher.deleted:
                teacher_dict.append(teacher.dict())

        return {'status': 'ok', 'data': teacher_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            teacher = Teacher.get(pk)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        teacher.deleted = 1
        teacher.save()

        return {'status': 'ok', 'data': teacher.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        try:
            teacher = Teacher.get(pk)
            print(teacher)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        teacher.name = args['name']
        teacher.phone = args['phone']
        teacher.deleted = 0
        teacher.save()

        return {'status': 'ok', 'data': teacher.dict()}

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

        teacher = Teacher(**data)
        teacher.save()

        return {'status': 'ok', 'data': teacher.dict()}