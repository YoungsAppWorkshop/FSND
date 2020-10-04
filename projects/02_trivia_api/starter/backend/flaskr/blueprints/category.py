from flask import Blueprint, jsonify

bp = Blueprint("category", __name__)


@bp.route("/categories")
def categories():
    '''Endpoint to handle GET requests for all available categories.
    '''
    return jsonify({'status': 'success'}), 200
