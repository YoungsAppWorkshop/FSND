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
    req_body = json.loads(request.data)
    previous_questions = req_body.get('previous_questions')
    quiz_category = req_body.get('quiz_category')

    try:
        question = Question.query.filter_by(category=quiz_category['id']).filter(
            not_(Question.id.in_(previous_questions))).order_by(func.random()).first()

        data = {
            'question': question.format,
        }
    except:
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data)
