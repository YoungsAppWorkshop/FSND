from flask import Flask, jsonify
from flask_cors import CORS

from .setup_db import setup_db
from .utils import generate_response


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
    @app.errorhandler(400)
    def bad_request(error):
        return generate_response(400, 'Bad Request')

    @app.errorhandler(404)
    def not_found(error):
        return generate_response(404, 'Not Found')

    @app.errorhandler(416)
    def out_of_range(error):
        return generate_response(416, 'Requested Range Not Satisfiable')

    @app.errorhandler(422)
    def unprocessable(error):
        return generate_response(422, 'Unprocessable Entity')

    @app.errorhandler(500)
    def internal_server_error(error):
        return generate_response(500, 'Internal Server Error')

    # Register Blueprints
    from .blueprints import category, question
    app.register_blueprint(category.bp)
    app.register_blueprint(question.bp)

    return app
