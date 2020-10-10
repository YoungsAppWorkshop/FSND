import json
from flask import abort, Blueprint, request
from marshmallow import ValidationError

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
def add_or_search_questions():
    '''POST endpoint to add or search questions
        - Request Params
            - searchTerm: Search and return questions containing the search term
            - question, answer, difficulty, category: Add a new question
    '''
    req_body = json.loads(request.data)
    search_term = req_body.get('searchTerm')
    if search_term is not None:
        return search_questions(search_term)
    return add_a_new_question(req_body)


def add_a_new_question(payload):
    '''Add a new question
        - Payload: A dict containing question, answer, difficulty, category field
        - Returns: A new question
    '''
    try:
        new_question = QuestionSchema().load(payload)
        db.session.add(new_question)
        db.session.commit()
        data = {'question': new_question.format}
    except ValidationError:
        abort(400)
    except:
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data, status=201)


def search_questions(keyword: str):
    '''Search and return the questions which contain keywords
    '''
    try:
        questions = Question.query.filter(
            Question.question.ilike(f'%{keyword}%')).all()
        data = {
            'questions': [q.format for q in questions],
            'totalQuestions': len(questions),
        }
    except:
        abort(500)
    finally:
        db.session.close()
    return generate_response(data=data, status=200)
