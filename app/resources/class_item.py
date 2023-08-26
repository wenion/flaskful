from flask_restful import Resource, reqparse
from redis_om.model import NotFoundError
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

import datetime
from models import ClassItem

class ClassItemController(Resource):
    @jwt_required()
    def get(self):
        # print('current_user', current_user)
        class_items = ClassItem.find().all()

        class_item_dict =[]

        for class_item in class_items:
            if not class_item.deleted:
                class_item_dict.append(class_item.dict())

        return {'status': 'ok', 'data': class_item_dict}

    @jwt_required()
    def delete(self, pk):
        try:
            class_item = ClassItem.get(pk)
            print(class_item)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 200

        class_item.deleted = 1
        class_item.save()

        return {'status': 'ok', 'data': class_item.dict()}

    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('item_no', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('item_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('current_price', type=str, required=True,
                            help='This field cannot be left blank')
        # parser.add_argument('rate', type=str, required=True,
        #                     help='This field cannot be left blank')
        parser.add_argument('gst_included', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('comments', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()
        try:
            class_item = ClassItem.get(pk)
            print(class_item)
        except NotFoundError:
            return {'status': 'error', 'error': repr(NotFoundError)}, 400

        class_item.item_no = args['item_no']
        class_item.item_name = args['item_name']
        class_item.current_price = float(args['current_price'])
        # class_item.rate = float(args['rate'])
        class_item.gst_included = float(args['gst_included'])
        class_item.comments = args['comments']
        class_item.deleted = 0
        class_item.save()

        return {'status': 'ok', 'data': class_item.dict()}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_no', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('item_name', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('current_price', type=str, required=True,
                            help='This field cannot be left blank')
        # parser.add_argument('rate', type=str, required=True,
        #                     help='This field cannot be left blank')
        parser.add_argument('gst_included', type=str, required=True,
                            help='This field cannot be left blank')
        parser.add_argument('comments', type=str, required=True,
                            help='This field cannot be left blank')
        args = parser.parse_args()

        rate = 11.11
        gst_included = float(args['current_price']) * rate /100

        print("args", args)

        data = {
            'item_no': args['item_no'],
            'item_name': args['item_name'],
            'current_price': float(args['current_price']),
            'rate': rate,
            'gst_included': gst_included,
            'comments': args['comments']
        }

        class_item = ClassItem(**data)
        class_item.save()

        return {'status': 'ok', 'data': class_item.dict()}