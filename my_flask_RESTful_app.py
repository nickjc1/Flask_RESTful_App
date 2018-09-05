from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item():
    def __init__(self, name, price):
        self.name = name
        self.price = price


class My_item(Resource):

    @jwt_required()
    def get(self, name):
        the_item = next(filter(lambda item: item.name == name, items), None)
        if the_item:
            return {name: the_item.price}, 201
        else:
            return None, 404

    def post(self, name):
        if next(filter(lambda item: item.name == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        newItem = Item(name, data['price'])
        items.append(newItem)
        return {'message': 'new item ' + name + 'added into our database'}, 201

class My_item_list(Resource):
    def __init__(self):
        self.items_dic = []

    def get(self):
        for item in items:
            self.items_dic.append({item.name: item.price})
        return {"items": self.items_dic}

api.add_resource(My_item, '/item/<string:name>')
api.add_resource(My_item_list, '/items')
app.run(debug = True)
