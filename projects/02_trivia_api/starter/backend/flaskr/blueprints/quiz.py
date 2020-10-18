import json
from flask import abort, Blueprint, request
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import not_

from ..models import Question
from ..utils import generate_response
from ..setup_db import db


bp = Blueprint("quiz", __name__)


@bp.route("/quizzes", methods=['POST'])
def questions():
    '''POST endpoint to get questions to play the quiz.
        - Request Arguments: category, previous questions
        - Returns: A random question
    '''
    try:
        req_body = json.loads(request.data)
        previous_questions = req_body.get('previous_questions')
        quiz_category = req_body.get('quiz_category')['id']
    except Exception:
        abort(400)

    queries = []
    if quiz_category != 0:
        queries.append(Question.category == quiz_category)
    queries.append(not_(Question.id.in_(previous_questions)))

    try:
        question = Question.query.filter(
            *queries).order_by(func.random()).first()
        data = {
            'question': question.format,
        }
    except AttributeError:
        data = {}
    except Exception:
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data)
