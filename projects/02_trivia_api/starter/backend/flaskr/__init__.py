from flask import Flask, jsonify
from flask_cors import CORS

from .setup_db import setup_db

QUESTIONS_PER_PAGE = 10


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
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'status': 500,
            'message': 'Internal Server Error',
            'data': {},
        })

    # Register Blueprints
    from .blueprints import category
    app.register_blueprint(category.bp)

    return app
