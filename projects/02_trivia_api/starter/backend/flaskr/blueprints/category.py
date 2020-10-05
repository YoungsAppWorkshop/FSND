from flask import abort, Blueprint

from ..models import Category
from ..utils import aggregate_categories, generate_response
from ..setup_db import db

bp = Blueprint("category", __name__)


@bp.route("/categories")
def categories():
    '''Endpoint to handle GET requests for all available categories.
        - Fetches a dictionary of categories in which the keys are the ids and
          the value is the corresponding string of the category
        - Request Arguments: None
        - Returns: An object with a single key, categories, that contains a
          object of id: category_string key:value pairs.
    '''
    try:
        data = aggregate_categories(Category.query.all())
    except:
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data)
