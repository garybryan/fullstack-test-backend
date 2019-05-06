import json

from flask import Flask
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# Load stores data into memory.
with open('stores.json') as f:
    STORES = json.load(f)


LOWERCASE_STORES = [{key: val.lower() for key, val in store.items()} for store in STORES]


parser = reqparse.RequestParser()
parser.add_argument('search')


def search_stores(search):
    search = search.lower()
    matching_postcode = []
    matching_name = []
    for index, store in enumerate(LOWERCASE_STORES):
        # Stores matching postcode should be returned before ones matching name.
        if search in store['postcode'].lower():
            matching_postcode.append(STORES[index])
        elif search in store['name'].lower():
            matching_name.append(STORES[index])
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
