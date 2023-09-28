from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from app.models import Level

class LevelController(Resource):
    # @jwt_required()
    def get(self):
        # print('current_user', current_user)
        levels = Level.find(Level.deleted == 0).sort_by('id').all()

        level_dict =[]

        for level in levels:
            level_dict.append(level.dict())

        return {'status': 'ok', 'data': level_dict}

    @jwt_required()
    def delete(self, pk):
        print("delete", pk)
        try:
            level = Level.get(pk)
            print(level)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        level.deleted = 1
        level.save()

        return {'status': 'ok', 'data': level.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('abbreviation', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('start_age', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_age', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('display', type=int, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        try:
            level = Level.get(pk)
            print(level)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400
        else:
            level.name = args['name']
            level.level = args['name']
            level.abbreviation = args['abbreviation']
            level.start_age = args['start_age']
            level.end_age = args['end_age']
            level.display = args['display']
            level.deleted = 0
            level.save()
            # print('final leve', level)

            return {'status': 'ok', 'data': level.dict()}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('abbreviation', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('start_age', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_age', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        data = {
            'id': len(Level.find().all()) + 1,
            'name': args['name'],
            'level': args['name'],
            'abbreviation': args['abbreviation'],
            'start_age': args['start_age'],
            'end_age': args['end_age']
        }

        level = Level(**data)
        level.save()

        return {'status': 'ok', 'data': level.dict()}