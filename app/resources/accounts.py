from flask_restful import Resource, reqparse, abort
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required

from datetime import datetime, timezone, timedelta
from app.authenticate import RoleType, Permission
from app.models import User, Teacher, Student

class AuthController(Resource):
    # Login
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        parser.add_argument('password', type=str, required=True, location='form',
                            help='This field cannot be left blank')

        args = parser.parse_args()
        # print('args', args)

        user_auth = args['email'].lower()
        password = args['password']

        exist = User.find(User.email == user_auth).all()
        # print('exist', exist)
        if not len(exist):
            return {'status': '', 'message': 'Wrong username or password.'}, 401
            # exist = User.find(User.phone == user_auth).all()
            # if not len(exist):
            #     return {'status': '', 'message': 'Wrong username or password.'}, 401

        if len(exist) and exist[0]:
            user = exist[0]
            try:
                if user.role_type == RoleType.TEACHER:
                    binding_account = Teacher.get(user.binding_account).dict()
                elif user.role_type == RoleType.STUDENT:
                    binding_account = Student.get(user.binding_account).dict()
                else:
                    binding_account = {
                        'label': 'N/A',
                        'value': '0'
                    }
            except NotFoundError:
                binding_account = {
                    'label': 'Binding Account field is invaild',
                    'value': '0'
                }
            user_item = user.dict()
            user_item['binding_account'] = binding_account

            authorized = user.check_password(password)
            # print('authorized', authorized)
            if authorized:
                expires = timedelta(days=7)
                access_token = create_access_token(identity=user, expires_delta=expires)
                data = {
                    'profile': user_item,
                    'access_token': access_token,
                }
                return {'status': '', 'message': 'Login successfully.', 'data': data}, 200

        return {'status': '', 'message': 'Wrong username or password.'}, 401


class ProfileController(Resource):
    @jwt_required()
    def get(self, pk):
        print("pk", pk)

        return {'status': 'ok', 'data': []}

    @jwt_required()
    def delete(self, pk):
        

        return {'status': 'ok', 'data': []}

    @jwt_required()
    def put(self, pk):

        return {'status': 'ok', 'data': []}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()

        return {'status': 'ok', 'data': []}