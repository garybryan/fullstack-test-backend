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
parser.add_argument('offset', type=int)
parser.add_argument('limit', type=int)


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
        any_remaining = False
        if args['search']:
            stores = search_stores(search)
        else:
            stores = STORES
        if args['offset'] is not None or args['limit'] is not None:
            offset = args['offset'] or 0
            limit = offset + args['limit'] if args['limit'] is not None else None
            limit_slice = slice(offset, limit)
            num_stores = len(stores) - offset - limit
            stores = stores[limit_slice]
            if limit is not None:
                any_remaining = num_stores > limit
        return {
            'stores': stores,
            'anyRemaining': any_remaining,
        }


api.add_resource(Stores, '/stores')
