from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.item import ItemModel
import re
from datetime import datetime


class Item(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

    def post(self, date):
        parser =reqparse.RequestParser()
        parser.add_argument('title',
            type = str,
            required = True,
            help = "this field cannot be left blank"
        )    
        parser.add_argument('text',
            type=str,
            required = True,
            help = "Every item needs a text"
        )
        regex = re.compile("^(\d{4})-(0[1-9]|1[0-2]|[1-9])-([1-9]|0[1-9]|[1-2]\d|3[0-1])$")
        match = re.match(regex, date)
        if match:
            if ItemModel.find_by_date(date):
                return {'message':"An item with name '{}' already exists.".format(date)}, 400        
            data = parser.parse_args()

            item = ItemModel(date, data['title'], data['text'])
            try:
                item.save_to_db()
            except:
                return {'message':'An error occurred inserting the item. '}, 500 
            return item.json(), 201
        else:
            return {'message': f'Current Date does not match. please include an - in the date. {date} is missing an - .'}, 400

    def delete(self, id):
        item = ItemModel.find_by_id(id)
        if item is None:
            return {"message": 'Item not found'}, 404
        else:
            item.delete_from_db()            
        return {'message':'Item deleted'}

    def put(self, id):
        parser =reqparse.RequestParser()
        parser.add_argument('date',
            type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
            required = True,
            help = "Every item needs a date"
        )
        parser.add_argument('title',
            type = str,
            required = True,
            help = "this field cannot be left blank"
        )    
        parser.add_argument('text',
            type=str,
            required = True,
            help = "Every item needs a text"
        )
        data = parser.parse_args()        
        item = ItemModel.find_by_id(id)
    
        if item is None:
            return {"message": 'Item not found'}, 404
        else:
            item.date, item.title, item.text = data['date'], data['title'], data['text']
        item.save_to_db()
        return item.json()


