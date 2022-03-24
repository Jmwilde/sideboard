import os
import json
from flask import Flask, jsonify, abort, request
from models import db, setup_db, Merchant, Item, Customer
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import HTTPException
from config import Config
from auth import requires_auth, AuthError

def create_app(config=Config):

    app = Flask(__name__)
    setup_db(app, config)
    CORS(app)

    @app.route('/', methods=['GET'])
    def hello():
        return "Welcome to SideBoard!"

### MERCHANTS ###

    @app.route('/merchants', methods=['GET'])
    @requires_auth(permission='get:merchants')
    def get_merchants():
        merchants = Merchant.query.all()
        merchants_json = json.dumps([merchant.format() for merchant in merchants])

        return jsonify({
            'success': True,
            'merchants': merchants_json
        })

    @app.route('/merchants', methods=['POST'])
    @requires_auth(permission='create:merchants')
    def create_merchant():
        body = json.loads(request.data)
        merchant = Merchant(**body)
        merchant.insert()
        return jsonify({
            'success': True,
            'merchant': merchant.format()
        })

    @app.route('/merchants/<int:merchant_id>', methods=['PATCH'])
    @requires_auth(permission='patch:merchants')
    def edit_merchant(merchant_id):
        merchant = Merchant.query.filter(Merchant.id == merchant_id).one_or_none()
        if not merchant:
            abort(404)

        body = json.loads(request.data)
        # PATCH: Update only the fields found in the request
        merchant.update(**body)
        return jsonify({
            'success': True,
            'merchant': merchant.format()
        })

    @app.route('/merchants/<int:merchant_id>', methods=['DELETE'])
    @requires_auth(permission='delete:merchants')
    def delete_merchant(merchant_id):
        merchant = Merchant.query.get(merchant_id)
        if not merchant:
            abort(404)
        merchant.delete()
        return jsonify({
            'success': True,
            'merchant': merchant.format()
        })

### ITEMS ###

    @app.route('/items', methods=['GET'])
    @requires_auth(permission='get:items')
    def get_items():
        items = Item.query.all()
        items_json = json.dumps([item.format() for item in items])
        return jsonify({
            'success': True,
            'items': items_json
        })

    @app.route('/items', methods=['POST'])
    @requires_auth(permission='create:items')
    def create_item():
        body = json.loads(request.data)
        item = Item(**body)
        item.insert()
        return jsonify({
            'success': True,
            'item': item.format()
        })

    @app.route('/items/<int:item_id>', methods=['PATCH'])
    @requires_auth(permission='patch:items')
    def edit_item(item_id):
        item = Item.query.filter(Item.id == item_id).one_or_none()
        if not item:
            abort(404)

        body = json.loads(request.data)
        item.update(**body)
        return jsonify({
            'success': True,
            'item': item.format()
        })

    @app.route('/items/<int:item_id>', methods=['DELETE'])
    @requires_auth(permission='delete:items')
    def delete_item(item_id):
        item = Item.query.get(item_id)
        if not item:
            abort(404)
        item.delete()
        return jsonify({
            'success': True,
            'item': item.format()
        })

### CUSTOMERS ###

    @app.route('/customers', methods=['GET'])
    @requires_auth(permission='get:customers')
    def get_customers():
        customers = Customer.query.all()
        customers_json = json.dumps([cust.format() for cust in customers])
        return jsonify({
            'success': True,
            'customers': customers_json
        })

    @app.route('/customers', methods=['POST'])
    @requires_auth(permission='create:customers')
    def create_customer():
        body = json.loads(request.data)
        customer = Customer(**body)
        customer.insert()
        return jsonify({
            'success': True,
            'customer': customer.format()
        })

    @app.route('/customers/<int:customer_id>', methods=['PATCH'])
    @requires_auth(permission='patch:customers')
    def edit_customer(customer_id):
        customer = Customer.query.filter(Customer.id == customer_id).one_or_none()
        if not customer:
            abort(404)

        body = json.loads(request.data)
        customer.update(**body)
        return jsonify({
            'success': True,
            'customer': customer.format()
        })

    @app.route('/customers/<int:customer_id>', methods=['DELETE'])
    @requires_auth(permission='delete:customers')
    def delete_customer(customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            abort(404)
        customer.delete()
        return jsonify({
            'success': True,
            'customer': customer.format()
        })

### Error handlers ###

    @app.errorhandler(SQLAlchemyError)
    def db_error(e):
        #print(f'{e = }')
        db.session.rollback()
        return jsonify({
            'success': False,
            'status': 409,
            'error': e.__class__.__name__,
            'message': 'Request conflicts with database constraints.'
        }), 409

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            'success': False,
            'status': e.status_code,
            'error': e.error['code'],
            'message': e.error['description']
        }), 401

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            'success': False,
            'status': e.code,
            'error': e.name,
            'message': e.description
        }), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'status': e.code,
            'error': e.name,
            'message': e.description
        }), 404

    @app.errorhandler(409)
    def conflict(e):
        return jsonify({
            'success': False,
            'status': e.code,
            'error': e.name,
            'message': e.description
        }), 409

    @app.errorhandler(500)
    def internal_server(e):
        return jsonify({
            'success': False,
            'status': e.code,
            'error': e.name,
            'message': e.description
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()