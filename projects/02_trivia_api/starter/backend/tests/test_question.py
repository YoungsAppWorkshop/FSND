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
