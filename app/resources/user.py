from flask_restful import Resource, reqparse, abort
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from redis_om.model import NotFoundError

from datetime import datetime, timezone

from app.models import User, Teacher, Student, UserRTeacher, UserRStudent
from app.authenticate import RoleType, Permission

class UserController(Resource):
    # @jwt_required()
    def get(self):
        users = User.find(User.deleted == 0).sort_by('id').all()
        user_dict =[]

        for user in users:
            # try:
            #     if user.role_type == RoleType.TEACHER:
            #         binding_account = Teacher.get(user.binding_account).dict()
            #     elif user.role_type == RoleType.STUDENT:
            #         binding_account = Student.get(user.binding_account).dict()
            #     else:
            #         binding_account = {
            #             'label': 'N/A',
            #             'value': '0'
            #         }
            # except NotFoundError:
            #     binding_account = {
            #         'label': 'Binding Account field is invaild',
            #         'value': '0'
            #     }
            if user.role_type == RoleType.TEACHER:
                exist = UserRTeacher.find(UserRTeacher.user == user.pk).all()
                if len(exist) > 0:
                    teacher = Teacher.get(exist[0].teacher)
                
            elif user.role_type == RoleType.STUDENT:
                t = UserRStudent.find(UserRStudent.user == user.pk).all()
                print("sss", t)
            
            

            user_item = user.dict()
            # user_item['binding_account'] = binding_account

            print("item", user_item)
            
            user_dict.append(user_item)

        return {'status': 'ok', 'data': user_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            user = User.get(pk)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        user.deleted = 1
        user.save()

        return {'status': 'ok', 'data': user.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('account_name', type=str, required=True,
                            help='This field cannot be left blank')
        # parser.add_argument('email', type=str, required=True,
        #                     help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('auth', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('role_type', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('binding_account', type=dict)
        parser.add_argument('password', type=str)
        parser.add_argument('display', type=int, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        try:
            user = User.get(pk)
        except NotFoundError:
            return abort(400, message=repr(NotFoundError))

        user.account_name = args['account_name']
        user.phone = args['phone']
        if int(args['auth']['value']) != Permission.LEVEL4:
            user.auth = int(args['auth']['value'])
        if args['password']:
            user.password = User.hash_password(args['password'])
        user.role_type = args['role_type']['value']
        if args['binding_account']:
            user.binding_account = args['binding_account']['value']
        else:
            user.binding_account = '0'
        user.display = args['display']
        user.deleted = 0
        user.save()

        user_item = user.dict()
        user_item['binding_account'] = args['binding_account']

        return {'status': 'ok', 'data': user_item}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('email', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('phone', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('password', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('auth', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('role_type', type=dict, required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('password', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('binding_account', type=dict, location='json')
        args = parser.parse_args()

        exist = User.find(User.email == args['email'].lower()).all()
        if len(exist) > 0:
            return abort(400, message='Email has been used')

        binding_account = '0'
        if args['binding_account']:
            binding_account = args['binding_account']['value']

        created = datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None)

        data = {
            'id': len(User.find().all()) + 1,
            'account_name': args['account_name'],
            'email': args['email'].lower(),
            'phone': args['phone'],
            'password': User.hash_password(args['password']),
            'binding_account': binding_account,
            'auth': args['auth']['value'],
            'role_type': args['role_type']['value'],
            'created': created,
            'updated': created,
        }

        user = User(**data)
        user.save()

        user_item = user.dict()
        user_item['binding_account'] = args['binding_account']

        return {'status': 'ok', 'data': user_item}