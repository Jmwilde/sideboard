import os
import json
from flask import Flask, jsonify, abort, request
from models import setup_db, Merchant, Item, Customer
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def hello():
        return "Hello World!"

    @app.route('/merchants', methods=['GET'])
    def get_merchants():
        try:
            merchants = Merchant.query.all()
            merchants_json = json.dumps([merchant.format() for merchant in merchants])
            return jsonify({
                'success': True,
                'merchants': merchants_json
            })
        except:
            abort(400)

    @app.route('/merchants', methods=['POST'])
    def create_merchant():
        try:
            body = json.loads(request.data)
            merchant = Merchant(**body)
            merchant.insert()
            return jsonify({
                'success': True,
                'merchant': merchant.format()
            })
        except IntegrityError as e:
            abort(409)
        except:
            abort(400)

    @app.route('/merchants/<int:merchant_id>', methods=['PATCH'])
    def edit_merchant(merchant_id):
        try:
            merchant = Merchant.query.filter(Merchant.id == merchant_id).one_or_none()
            if not merchant:
                abort(404)

            body = json.loads(request.data)
            # Patch means only update fields found in the request
            # Maps the request fields to the data model
            for k, v in body.items():
                print(f'{k = }')
                setattr(merchant, k, v)

            merchant.update()
            return jsonify({
                'success': True,
                'merchant': merchant.format()
            })
        # Handle requests that break db constraints
        except IntegrityError:
            abort(409)
        # Rethrow http exceptions
        except HTTPException as e:
            abort(e.code)
        except:
            abort(400)

    @app.route('/merchants/<int:merchant_id>', methods=['DELETE'])
    def delete_merchant(merchant_id):
        try:
            merchant = Merchant.query.get(merchant_id)
            if not merchant:
                abort(404)
            merchant.delete()
            return jsonify({
                'success': True,
                'merchant': merchant.format()
            })
        # Rethrow http exceptions
        except HTTPException as e:
            abort(e.code)
        except:
            abort(400)

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

    return app

app = create_app()

if __name__ == '__main__':
    app.run()