import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, setup_db
from flaskr.constants import QUESTIONS_PER_PAGE
from flaskr.models import Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_fetch_categories(self):
        """
        Test handling GET requests for all available categories
        : GET /categories
        """
        res = self.client().get('/categories')

        payload = json.loads(res.data)
        expected = {
            'status': 200,
            'message': 'OK',
            'data': {
                '1': "Science",
                '2': "Art",
                '3': "Geography",
                '4': "History",
                '5': "Entertainment",
                '6': "Sports",
            },
        }

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload, expected)

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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
