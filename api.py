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


def search_stores(search):
    search = search.lower()
    # TODO match postcode first
    matching_postcode = []
    matching_name = []
    for store in STORES:
        if search in store['postcode'].lower():
            matching_postcode.append(store)
        elif search in store['name'].lower():
            matching_name.append(store)
    return matching_postcode + matching_name


class Stores(Resource):
    def get(self):
        args = parser.parse_args()
        search = args['search']
        if args['search']:
            stores = search_stores(search)
        else:
            stores = STORES
        return stores


api.add_resource(Stores, '/stores')
