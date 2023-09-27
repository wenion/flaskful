from flask_restful import Resource, reqparse, abort
from flask import jsonify

from datetime import datetime, timezone
from authenticate import RoleType, Permission
from models import User

class SignupController(Resource):
    # def __init__(self):
    #     self.logger = create_logger()

    # parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    # parser.add_argument('username', type=str, required=True,
    #                     help='This field cannot be left blank')
    # parser.add_argument('password', type=str, required=True,
    #                     help='This field cannot be left blank')

    def post(self):
        print("post>>>")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        parser.add_argument('email', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        parser.add_argument('password', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        args = parser.parse_args()
        # print("parser",parser, args, args['email'].lower())

        exist = User.find(User.email == args['email'].lower()).all()
        if len(exist) > 0:
            return abort(400, message='User already exists')

        created = datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None)
        data = {
            'id': len(User.find().all()) + 1,
            'account_name': args['name'],
            'email': args['email'].lower(),
            'phone': '',
            'password': User.hash_password(args['password']),
            'auth': Permission.MINIMUM,
            'role_type': RoleType.USER,
            'binding_account': '0',
            'created': created,
            'updated': created,
            }

        user = User(**data)
        user.save()

        return {'status': 'ok', 'message': 'user has been created successfully.', 'data': user.dict()}, 201