import unittest

from api import app


class StoresTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client

    def test_get_stores(self):
        res = self.client().get('/stores')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data), 95)

    def test_search_store_name(self):
        res = self.client().get('/stores?search=hav')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data), 2)
        self.assertIn({"name": "Newhaven", "postcode": "BN9 0AG"}, data)
        self.assertIn({"name": "Havant", "postcode": "PO9 1ND"}, data)

    def test_search_store_ordering(self):
        res = self.client().get('/stores?search=br')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0], {'name': 'Orpington', 'postcode': 'BR5 3RP'})  # Only store with BR in postcode: should be first.
