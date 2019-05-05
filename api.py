import json

from flask import Flask
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)

# Load stores data into memory.
with open('stores.json') as f:
    STORES = json.load(f)


parser = reqparse.RequestParser()
parser.add_argument('search')


class Stores(Resource):
    def get(self):
        args = parser.parse_args()
        search = args['search']
        if args['search']:
            # Very simple linear search to start off with.
            search = search.lower()
            stores = [store for store in STORES if search in store['postcode'] or search in store['name'].lower()]
        else:
            stores = STORES
        return stores


api.add_resource(Stores, '/stores')
