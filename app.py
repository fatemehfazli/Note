
from flask import Flask
from flask_restful import Api
from datetime import timedelta
from resources.item import Item


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item,'/item/<string:date>', methods=['post'], endpoint='item')
api.add_resource(Item, '/itemdelete/<int:id>', methods=['delete'], endpoint='itemdelete')
api.add_resource(Item, '/itemput/<int:id>', methods=['put'], endpoint='itemput')
api.add_resource(Item, '/items' ,methods=['get'], endpoint='items')

from db import db
db.init_app(app)
if __name__ == '__main__':

    app.run(port=5000, debug=True)