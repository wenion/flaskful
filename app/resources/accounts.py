from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token

import datetime
from models import User

class AuthController(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        parser.add_argument('password', type=str, required=True, location='form',
                            help='This field cannot be left blank')

        # parser.add_argument('email')
        # parser.add_argument('password')

        args = parser.parse_args()
        print('args', args)

        user_auth = args['email'].lower()
        password = args['password']

        exist = User.find(User.email == user_auth).all()
        print('exist', exist)
        if not len(exist):
            exist = User.find(User.phone == user_auth).all()
            if not len(exist):
                return {'status': '', 'message': 'Wrong username or password.'}, 401

        if len(exist) and exist[0]:
            user = exist[0]
            authorized = user.check_password(password)
            print('authorized', authorized)
            if authorized:
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(identity=user, expires_delta=expires)
                data = {
                    'userid': user.userid,
                    'email': user.email,
                    'phone': user.phone,
                    'access_token': access_token,
                }
                return {'status': '', 'message': 'Login successfully.', 'data': data}, 200

        return {'status': '', 'message': 'Wrong username or password.'}, 401