from flask import abort, Blueprint, request
from flaskr.models.exceptions import ParamsOutOfRange

from ..constants import QUESTIONS_PER_PAGE
from ..models import Category, Question
from ..setup_db import db
from ..utils import aggregate_categories, generate_response

bp = Blueprint("question", __name__)


@bp.route("/questions")
def questions():
    '''Endpoint to handle GET requests for fetching questions
        - Request Arguments: Page number
        - Returns: List of questions, Number of questions and Categories
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    try:
        categories = Category.query.all()
        questions = Question.query.all()

        if start > len(questions):
            raise ParamsOutOfRange

        data = {
            'questions': [q.format for q in questions[start:end]],
            'total_questions': len(questions),
            'categories': aggregate_categories(categories)
        }
    except ParamsOutOfRange:
        abort(422)
    except:
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data)


@bp.route("/questions/<int:question_id>", methods=['DELETE'])
def delete_question(question_id):
    '''Endpoint to DELETE a question using a question ID
        - Request Arguments: A question ID
        - Returns: Question ID of the deleted question
    '''
    try:
        Question.query.get(question_id).delete()
        db.session.commit()
        data = {'id': question_id}
    except AttributeError:
        db.session.rollback()
        abort(422)
    except:
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data)


'''
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
'''

'''
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
'''

'''
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
'''

'''
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
'''
