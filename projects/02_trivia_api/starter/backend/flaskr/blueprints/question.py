import json
from flask import abort, Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.log import class_logger


from ..constants import QUESTIONS_PER_PAGE
from ..exceptions import OutOfRange
from ..models import Category, Question
from ..schemas import QuestionSchema
from ..utils import aggregate_categories, generate_response
from ..setup_db import db

bp = Blueprint("question", __name__)


@bp.route("/questions")
def questions():
    '''Endpoint to handle GET requests for fetching questions
        - Query Params: page
        - Returns: List of questions, Number of questions and Categories
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    try:
        categories = Category.query.all()
        questions = Question.query.all()

        if start > len(questions):
            raise OutOfRange()

        data = {
            'questions': [q.format for q in questions[start:end]],
            'total_questions': len(questions),
            'categories': aggregate_categories(categories)
        }
    except OutOfRange:
        abort(416)
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


@bp.route("/categories/<int:category_id>/questions")
def questions_by_category(category_id):
    '''GET endpoint to get questions based on category
        - Request Arguments: category_id
        - Query Params: page
        - Returns: List of questions, Number of questions and category
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    try:
        questions = Question.query.filter_by(category=category_id).all()

        if start > len(questions):
            raise OutOfRange()

        data = {
            'questions': [q.format for q in questions[start:end]],
            'total_questions': len(questions),
            'current_category': category_id
        }
    except OutOfRange:
        abort(416)
    except:
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data)


@bp.route("/questions", methods=['POST'])
def add_a_new_question():
    '''POST endpoint to add a question
        - Request Body: question, answer, difficulty, category
        - Returns: A new question
    '''
    try:
        req_body = json.loads(request.data)
        new_question = QuestionSchema().load(req_body)
        db.session.add(new_question)
        db.session.commit()
        data = {'question': QuestionSchema().dump(new_question)}
    except ValidationError:
        abort(400)
    except:
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data, status=201)


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
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
'''
