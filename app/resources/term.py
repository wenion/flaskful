from flask_restful import Resource, reqparse, inputs
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from dateutil import parser as date_parser
from dateutil.tz import tzutc
import pytz
from models import Term

class TermController(Resource):
    # @jwt_required()
    def get(self):
        # print('current_user', current_user)
        terms = Term.find(Term.deleted == 0).sort_by('id').all()

        term_dict =[]

        for term in terms:
            term_dict.append(term.dict())

        return {'status': 'ok', 'data': term_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            term = Term.get(pk)
            print(term)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        term.deleted = 1
        term.save()

        return {'status': 'ok', 'data': term.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('year', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('number_of_week', type=int, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('start_day', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_day', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('display', type=int, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        try:
            term = Term.get(pk)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400
        
        # start_day = datetime.strptime(args['start_day'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # end_day = datetime.strptime(args['end_day'], "%Y-%m-%dT%H:%M:%S.%fZ")

        # start_day = start_day.replace(tzinfo=timezone.utc).astimezone(tz=None).date()
        # end_day = end_day.replace(tzinfo=timezone.utc).astimezone(tz=None).date()
        # print("start", args['start_day'])
        # print("end",args['end_day'])
        start_day = date_parser.parse(args['start_day'])#.replace(tzinfo=tzutc())
        end_day = date_parser.parse(args['end_day'])#.replace(tzinfo=tzutc())

        term.name = args['name']
        term.year = args['year']
        term.number_of_week = args['number_of_week']
        term.start_day = start_day
        term.end_day = end_day
        term.display = args['display']
        term.deleted = 0
        term.save()

        return {'status': 'ok', 'data': term.dict()}
        # return {'status': 'ok', 'data': []}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('year', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('number_of_week', type=int, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('start_day', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_day', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        # print("post", args['start_day'])

        # start_day = datetime.strptime(args['start_day'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # end_day = datetime.strptime(args['end_day'], "%Y-%m-%dT%H:%M:%S.%fZ")

        # start_day = start_day.replace(tzinfo=timezone.utc).astimezone(tz=None).date()
        # end_day = end_day.replace(tzinfo=timezone.utc).astimezone(tz=None).date()
        start_day = date_parser.parse(args['start_day'])#.replace(tzinfo=tzutc())
        end_day = date_parser.parse(args['end_day'])#.replace(tzinfo=tzutc())
        # print("start", start_day)
        # print("start", start_day.astimezone(pytz.timezone("Australia/Sydney")))

        data = {
            'id': len(Term.find().all()) + 1,
            'name': args['name'],
            'year': args['year'],
            'number_of_week': args['number_of_week'],
            'start_day': start_day,
            'end_day': end_day,
        }

        term = Term(**data)
        term.save()

        return {'status': 'ok', 'data': term.dict()}