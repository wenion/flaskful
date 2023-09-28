from flask_restful import Resource, reqparse, abort
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from datetime import datetime, timezone
from app.models import Teacher, User
from app.authenticate import Permission, RoleType

class TeacherController(Resource):
    @jwt_required()
    def get(self):
        teachers = Teacher.find(Teacher.deleted == 0).sort_by('id').all()

        teacher_dict =[]

        for teacher in teachers:
            teacher_dict.append(teacher.dict())

        return {'status': 'ok', 'data': teacher_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            teacher = Teacher.get(pk)
        except NotFoundError:
            return abort(400, message='Account has been deleted')

        # TODO

        teacher.deleted = 1
        teacher.save()

        return {'status': 'ok', 'data': teacher.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('dob', type=str)
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('wechat', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('user_account', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        
        parser.add_argument('display', type=int, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        try:
            teacher = Teacher.get(pk)
        except NotFoundError:
            return abort(400, message=repr(NotFoundError))

        teacher.name = args['name']
        teacher.phone = args['phone']
        teacher.wechat = args['wechat']
        teacher.user_account = args['user_account']['value']
        teacher.updated = datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None)
        teacher.display = args['display']
        teacher.deleted = 0
        teacher.save()

        return {'status': 'ok', 'data': teacher.dict()}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('dob', type=str)
        parser.add_argument('email', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('wechat', type=str, required=True,
                            help='This field cannot be left blank')
        # parser.add_argument('lessons', type=list[str], required=True,
        #                     help='This field cannot be left blank', location='json')
        # parser.add_argument('user_account', type=str, required=True,
        #                     help='This field cannot be left blank')
        args = parser.parse_args()

        created = datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None)
        if args['dob']:
            dob = datetime.strptime(args['dob'], "%Y-%m-%dT%H:%M:%S.%fZ")
            dob = dob.replace(tzinfo=timezone.utc).astimezone(tz=None)
        else:
            dob = created

        exist = Teacher.find(Teacher.email == args['email'].lower()).all()
        if len(exist) > 0:
            return abort(400, message='Email has been used')

        data = {
            'id': len(Teacher.find().all()) + 1,
            'name': args['name'],
            'dob': dob,
            'email': args['email'].lower(),
            'phone': args['phone'],
            'wechat': args['wechat'],
            'role_type': RoleType.TEACHER,
            'lessons': [],
            'user_account': '',
            'created': created,
            'updated': created,
        }

        teacher = Teacher(**data)
        # teacher.save()

        user_data = {
            'id': len(User.find().all()) + 1,
            'account_name': args['name'],
            'email': args['email'].lower(),
            'phone': args['phone'],
            'password': User.hash_password(args['phone']),
            'auth': Permission.LEVEL3,
            'role_type': RoleType.TEACHER,
            'binding_account': teacher.pk,
            'created': created,
            'updated': created,
        }

        exist = User.find(User.email == args['email'].lower()).all()
        if len(exist) == 0:
            user = User(**user_data)
            user.save()
        else:
            user = exist[0]

        teacher.user_account = user.pk
        teacher.save()

        return {'status': 'ok', 'data': teacher.dict()}