import json

from flaskr.constants import QUESTIONS_PER_PAGE
from tests.test_flaskr import TriviaTestCase


class QuestionTestCase(TriviaTestCase):
    def test_fetch_questions_without_params(self):
        """
        Test handling GET requests for questions without page parameter
        : GET /questions
        """
        res = self.client().get('/questions')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload['message'], 'OK')
        self.assertEqual(len(payload['data']['questions']), QUESTIONS_PER_PAGE)

    def test_fetch_questions_with_params(self):
        """
        Test handling GET requests for questions with page parameter
        : GET /questions?page=1
        """
        res = self.client().get('/questions?page=1')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload['message'], 'OK')
        self.assertEqual(len(payload['data']['questions']), QUESTIONS_PER_PAGE)

    def test_fetch_questions_with_params_out_of_range(self):
        """
        Test handling GET requests for questions with page parameter out of range
        : GET /questions?page=3
        """
        res = self.client().get('/questions?page=3')

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(payload['message'], 'Unprocessable Entity')
