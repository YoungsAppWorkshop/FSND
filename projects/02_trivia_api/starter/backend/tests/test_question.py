import json

from flaskr.constants import QUESTIONS_PER_PAGE
from flaskr.models import Question
from tests.test_flaskr import TriviaTestCase


class QuestionTestCase(TriviaTestCase):
    def test_fetch_questions_without_params(self):
        """Test handling GET requests for questions without a page parameter
            : GET /questions
        """
        res = self.client().get('/questions')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload['message'], 'OK')
        self.assertEqual(len(payload['data']['questions']), QUESTIONS_PER_PAGE)

    def test_fetch_questions_with_params(self):
        """Test handling GET requests for questions with a page parameter
            : GET /questions?page=1
        """
        EXISTING_PAGE_NUMBER = 1
        res = self.client().get(f'/questions?page={EXISTING_PAGE_NUMBER}')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload['message'], 'OK')
        self.assertEqual(len(payload['data']['questions']), QUESTIONS_PER_PAGE)

    def test_fetch_questions_with_invalid_params(self):
        """Test handling GET requests for questions with an invalid parameter
            : GET /questions?page=3
        """
        NON_EXISTING_PAGE_NUMBER = 3
        res = self.client().get(f'/questions?page={NON_EXISTING_PAGE_NUMBER}')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 416)
        self.assertEqual(payload['message'], 'Requested Range Not Satisfiable')

    def test_delete_question(self):
        """Test handling DELETE question request for an existing question
            : DELETE /questions/<int:id>
        """
        EXISTING_QUESTION_ID = 2
        res = self.client().delete(f'/questions/{EXISTING_QUESTION_ID}')

        payload = json.loads(res.data)
        question = Question.query.get(EXISTING_QUESTION_ID)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload['data']['id'], EXISTING_QUESTION_ID)
        self.assertEqual(question, None)

    def test_delete_non_existing_question(self):
        """Test handling DELETE question request for a non-existing question
            : DELETE /questions/<int:id>
        """
        NON_EXISTING_QUESTION_ID = 1
        res = self.client().delete(f'/questions/{NON_EXISTING_QUESTION_ID}')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(payload['message'], 'Unprocessable Entity')

    def test_fetch_questions_by_category(self):
        """Test handling GET requests for questions of a category
            : GET /categories/<int:category_id>/questions
        """
        CATEGORY_ID = 1
        res = self.client().get(f'/categories/{CATEGORY_ID}/questions')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload['message'], 'OK')

    def test_fetch_questions_by_category_with_invalid_page_number(self):
        """Test handling GET requests for questions of a category with an
        invalid parameter
            : GET /categories/<int:category_id>/questions?page=999
        """
        INVALID_PAGE_NUMBER = 999
        CATEGORY_ID = 1
        res = self.client().get(
            f'/categories/{CATEGORY_ID}/questions?page={INVALID_PAGE_NUMBER}')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 416)
        self.assertEqual(payload['message'], 'Requested Range Not Satisfiable')

    def test_add_a_new_question(self):
        """Test handling POST requests to add a new question
            :POST /questions
        """
        res = self.client().post('/questions', json=dict(
            question='This is a Test Question. Is it working?',
            answer='Yes, it is.',
            difficulty='1',
            category='1',
        ))

        self.assertEqual(res.status_code, 201)

    def test_try_to_add_a_question_with_wrong_parameters(self):
        """Test to add a new question with wrong params
            :POST /questions
        """
        res = self.client().post('/questions', json=dict(
            wrong='This is a Test Question. Is it working?',
            params='No, it isnt.',
        ))

        self.assertEqual(res.status_code, 400)

    def test_search_questions(self):
        """Test to search questions containing some keywords
            :POST /questions
        """
        res = self.client().post('/questions', json=dict(
            searchTerm='title',
        ))

        payload = json.loads(res.data)
        expected = {
            "data": {
                "questions": [
                    {
                        "answer": "Maya Angelou",
                        "category": 4,
                        "difficulty": 2,
                        "id": 5,
                        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                    },
                    {
                        "answer": "Edward Scissorhands",
                        "category": 5,
                        "difficulty": 3,
                        "id": 6,
                        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                    }
                ],
                "totalQuestions": 2
            },
            "message": "OK",
            "status": 200
        }

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload, expected)

    def test_search_questions_using_wrong_keyword(self):
        """Test to search questions returns empty result
            :POST /questions
        """
        WRONG_KEYWORD = 'abkehui'
        res = self.client().post('/questions', json=dict(
            searchTerm=WRONG_KEYWORD,
        ))

        payload = json.loads(res.data)
        expected = {
            "data": {
                "questions": [],
                "totalQuestions": 0
            },
            "message": "OK",
            "status": 200
        }

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload, expected)

    def test_search_questions_using_wrong_path(self):
        """Test making API request to wrong path returns 404 Error
            :POST /questions
        """
        WRONG_PATH = '/question'
        res = self.client().post(WRONG_PATH, json=dict(
            searchTerm='title',
        ))

        payload = json.loads(res.data)
        expected = {
            'data': {},
            'message': 'Not Found',
            'status': 404,
        }

        self.assertEqual(res.status_code, 404)
        self.assertEqual(payload, expected)

    def test_search_questions_using_wrong_method(self):
        """Test making API request with wrong HTTP method returns 405 Error
            :POST /questions
        """
        res = self.client().put('/questions', json=dict(
            searchTerm='title',
        ))

        payload = json.loads(res.data)
        expected = {
            'data': {},
            'message': 'Method Not Allowed',
            'status': 405,
        }

        self.assertEqual(res.status_code, 405)
        self.assertEqual(payload, expected)
