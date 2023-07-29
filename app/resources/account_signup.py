from flask_restful import Resource, reqparse
from flask import jsonify

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
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        parser.add_argument('password', type=str, required=True, location='form',
                            help='This field cannot be left blank')
        args = parser.parse_args()
        print("parser",parser, args, args['email'].lower())
        
        exist = User.find(User.email == args['email'].lower()).all()
        if len(exist) > 0:
            return {'status': '', 'message': 'User has already been created, aborting.'}, 400
        
        data = {
            'userid': '',
            'email': args['email'].lower(),
            'phone': '',
            'password': User.hash_password(args['password'])}

        user = User(**data)
        user.save()

        return {'status': '', 'message': 'user has been created successfully.', 'pk': user.pk}, 201