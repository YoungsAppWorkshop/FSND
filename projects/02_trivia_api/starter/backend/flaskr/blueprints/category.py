from flask import Blueprint, jsonify

from ..models import Category
from ..utils import aggregate_categories
from ..setup_db import db

bp = Blueprint("category", __name__)


@bp.route("/categories")
def categories():
    '''
    Endpoint to handle GET requests for all available categories.

    GET '/categories'
        - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
        - Request Arguments: None
        - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
    '''
    try:
        categories = Category.query.all()
        res = {
            'status': 200,
            'message': 'OK',
            'data': aggregate_categories(categories)
        }
    except:
        res = {}
    finally:
        db.session.close()
    return jsonify(res)
