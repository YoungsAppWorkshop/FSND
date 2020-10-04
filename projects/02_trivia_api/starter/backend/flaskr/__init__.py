from flask import Flask, jsonify
from flask_cors import CORS

from .setup_db import setup_db


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Setup CORS
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        )
        return response

    # Error Handlers
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'status': 422,
            'message': 'Unprocessable Entity',
            'data': {},
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'status': 500,
            'message': 'Internal Server Error',
            'data': {},
        }), 500

    # Register Blueprints
    from .blueprints import category, question
    app.register_blueprint(category.bp)
    app.register_blueprint(question.bp)

    return app
