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
