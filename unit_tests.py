import os
import unittest
import json
import logging
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from config import TestConfig
from models import db, setup_db, Merchant, Item, Customer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SideboardTest(unittest.TestCase):
    """This class represents the sideboard test case"""

    dummy_merchant = {
        "name": "Dum Dicaprio",
        "city": "Los Angeles",
        "description": "I refurbish antique furniture into beautiful chic pieces.",
        "email": "dum@gumshoe.com",
        "phone": 1234567890,
        "state": "California"
    }

    dummy_item = {
        "name": "old chair",
        "price": 10.00,
        "description": "A funky antique chair",
        "merchant_id": 1
    }

    # Helpful info on correct setUp/tearDown:
    # blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
    def setUp(self):
        """Executed before each test"""
        """Define test variables and initialize app."""
        self.app = create_app(TestConfig)
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Executed after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_merchants(self):
        res = self.client().get('/merchants')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['merchants'])

    def test_get_merchants_404(self):
        res = self.client().get('/merchant')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_merchant(self):
        res = self.client().post('/merchants', json=self.dummy_merchant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['merchant']), 11)

    def test_create_merchant_409(self):
        # Using the same id twice
        res = self.client().post('/merchants', json=self.dummy_merchant)
        self.assertEqual(res.status_code, 200)

        # Should fail on the second try
        res = self.client().post('/merchants', json=self.dummy_merchant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)

    def test_edit_merchant(self):
        # Create a merchant
        merchant = Merchant(**self.dummy_merchant)
        merchant.insert()

        # Then edit a field
        merchant_json = {'name': 'Dee Dicaprio'}
        res = self.client().patch('/merchants/{}'.format(merchant.id), json=merchant_json)
        data = json.loads(res.data)

        self.assertEqual(data['merchant']['name'], 'Dee Dicaprio')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_merchant_404(self):
        # Edit non-existant merchant
        merchant_id = 1
        merchant_json = {'name': 'Dee Dicaprio'}
        res = self.client().patch('/merchants/{}'.format(merchant_id), json=merchant_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_merchant(self):
        # Create a merchant
        merchant = Merchant(**self.dummy_merchant)
        merchant.insert()

        # Then delete it
        res = self.client().delete('/merchants/{}'.format(merchant.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_merchant_404(self):
        merchant_id = 1
        res = self.client().delete('/merchants/{}'.format(merchant_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_items(self):
        res = self.client().get('/items')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['items'])
        self.assertEqual(len(data['items']), 2)

    def test_get_items_404(self):
        res = self.client().get('/item')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_item(self):
        # An item needs a valid merchant id so we generate one
        merchant = Merchant(**self.dummy_merchant)
        merchant.insert()

        # Copy the dummy item and update to a valid merchant id
        item_json = self.dummy_item.copy()
        item_json['merchant_id'] = merchant.id

        res = self.client().post('/items', json=item_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['item']), 5)
        self.assertEqual(data['success'], True)

    def test_create_item_409(self):
        # Using non-existing merchant id
        res = self.client().post('/items', json=self.dummy_item)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)

    def test_edit_item(self):
        # An item needs a valid merchant id so we generate one
        merchant = Merchant(**self.dummy_merchant)
        merchant.insert()

        # Copy the dummy item and update to a valid merchant id
        item_json = self.dummy_item.copy()
        item_json['merchant_id'] = merchant.id

        # Create an item
        item = Item(**item_json)
        item.insert()

        # Then edit a field
        name_field = {'name': 'New Table'}
        res = self.client().patch('/items/{}'.format(item.id), json=name_field)
        data = json.loads(res.data)

        self.assertEqual(data['item']['name'], 'New Table')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_item_404(self):
        # Edit non-existant item
        item_id = 1
        item_json = {'name': 'New Table'}
        res = self.client().patch('/items/{}'.format(item_id), json=item_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_item(self):
        # Create a merchant
        merchant = Merchant(**self.dummy_merchant)
        merchant.insert()

        # Create a new item
        item = Item(name='old chair', price='10.00', description='A funky antique chair', merchant_id=merchant.id)
        item.insert()

        # Then delete it
        res = self.client().delete('/items/{}'.format(item.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_item_404(self):
        item_id = 1
        res = self.client().delete('/items/{}'.format(item_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()