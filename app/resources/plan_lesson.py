from flask_restful import Resource, reqparse, inputs
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

from typing import Optional, List

from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser
from dateutil.tz import tzutc
import pytz
from models import Lesson, Term, ClassOption, get_num_from_day

# def switch_week_of_day(week_of_day)

def generate_dates(start_date, end_date, target_day, times):
    dates = []    
    # Convert the input strings to datetime objects
    start_date = start_date.astimezone(pytz.timezone("Australia/Sydney"))
    end_date = end_date.astimezone(pytz.timezone("Australia/Sydney"))
    
    # Calculate the day difference between the target day and the start day
    day_difference = (target_day - start_date.isoweekday() + 7) % 7
    resize_start_date = start_date + timedelta(days=day_difference)
    
    # Initialize the current date as the start date
    current_date = resize_start_date
    
    # Loop to generate dates within the range
    while current_date <= end_date:
        dates.append(current_date)
        if len(dates) == times:
            break
        current_date += timedelta(days=7)  # Add 7 days to move to the next week
    
    return dates


class PlanLessonController(Resource):
    def get(self, pk):
        try:
            class_option = ClassOption.get(pk).dict()
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        plan_lessons = Lesson.find(
            (Lesson.class_option_pk == pk) &
            (Lesson.deleted == 0)
        ).sort_by('id').all()

        plan_lesson_list = []
        term_dict = {}
        term_title = []

        for plan_lesson in plan_lessons:
            plan_lesson_dict = plan_lesson.dict()

            try:
                term = Term.get(plan_lesson.term_pk).dict()
            except NotFoundError:
                term = {
                    'label': 'Term field is invaild',
                    'value': 'invaild'
                    }
            print('term', term)
            if plan_lesson.term_pk not in term_dict:
                term_title.append(term)
                term_dict[plan_lesson.term_pk] = []
                term_dict[plan_lesson.term_pk].append(plan_lesson_dict)
            else:
                term_dict[plan_lesson.term_pk].append(plan_lesson_dict)
            plan_lesson_list.append(plan_lesson_dict)

        return {'status': 'ok',
            'data': {
                'request': class_option,
                'payload': plan_lesson_list,
                'terms': term_dict,
                'term_title': term_title,
                }}

    @jwt_required()
    def delete(self, pk):
        try:
            plan_lesson = Lesson.get(pk)
            print(plan_lesson)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        plan_lesson.deleted = 1
        plan_lesson.save()

        return {'status': 'ok', 'data': plan_lesson.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('class_code', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('location', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('day_of_week', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('start_time', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('end_time', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('level', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('terms', type=list[dict], required=True,
                            help='This field cannot be left blank', location='json')
        parser.add_argument('memeo', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        print("put args", args)
        try:
            plan_lesson = Lesson.get(pk)
            # print(plan_lesson)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        start_time = date_parser.parse(args['start_time'])
        end_time = date_parser.parse(args['end_time'])
        term_args = args['terms']
        term_list = [term['value'] for term in term_args if 'value' in term]

        plan_lesson.class_code = args['class_code']
        plan_lesson.location = args['location']
        plan_lesson.day_of_week = args['day_of_week']
        plan_lesson.start_time = start_time
        plan_lesson.end_time = end_time
        plan_lesson.terms = term_list
        plan_lesson.level = args['level']
        plan_lesson.memeo = args['memeo']
        plan_lesson.deleted = 0
        plan_lesson.save()

        return {'status': 'ok', 'data': plan_lesson.dict()}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('class_code', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('year', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('class_option_pk', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('term_pk', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        try:
            class_option = ClassOption.get(args['class_option_pk'])
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400
        
        try:
            term = Term.get(args['term_pk'])
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        lesson_list = []
        start_date = term.start_day
        end_date = term.end_day
        dates = generate_dates(start_date,
                               end_date,
                               get_num_from_day(class_option.day_of_week),
                               term.number_of_week
                               )
        week = 1
        for date in dates:
            print("item", date, )
            data = {
                'id': len(Lesson.find().all()) + 1,
                'class_option_pk': class_option.pk,
                'term_pk': term.pk,
                'class_code': class_option.class_code,
                'date': date,
                'year': term.year,
                'week': week,
                'teacher': '',
                'students': [],
            }
            week = week + 1

            plan_lesson = Lesson(**data)
            plan_lesson.save()
            lesson_list.append(plan_lesson.dict())

        # return {'status': 'ok', 'data': plan_lesson.dict()}
        return {'status': 'ok', 'data': {'request': class_option.dict(), 'payload': lesson_list}}