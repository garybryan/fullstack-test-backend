import json

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Load stores data into memory.
with open('stores.json') as f:
    STORES = json.load(f)


class Stores(Resource):
    def get(self):
        return STORES


api.add_resource(Stores, '/stores')
