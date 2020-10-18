import json

from tests.test_flaskr import TriviaTestCase


class QuizTestCase(TriviaTestCase):
    def test_api_returns_a_random_question(self):
        """Test fetching quiz returns a random question in the category
            : POST /quizzes
        """
        res = self.client().post('/quizzes', json=dict(
            previous_questions=[],
            quiz_category={'type': 'Sports', 'id': 6}
        ))

        payload = json.loads(res.data)
        one_of = [
            {
                "data": {
                    "question": {
                        "answer": "Brazil",
                        "category": 6,
                        "difficulty": 3,
                        "id": 10,
                        "question": "Which is the only team to play in every soccer World Cup tournament?"
                    }
                },
                "message": "OK",
                "status": 200
            },
            {
                "data": {
                    "question": {
                        "answer": "Uruguay",
                        "category": 6,
                        "difficulty": 4,
                        "id": 11,
                        "question": "Which country won the first ever soccer World Cup in 1930?"
                    }
                },
                "message": "OK",
                "status": 200
            }
        ]

        self.assertEqual(res.status_code, 200)
        self.assertIn(payload, one_of)

    def test_api_excludes_previous_questions(self):
        """Test fetching quiz returns a random question not in previous questions
            : POST /quizzes
        """
        res = self.client().post('/quizzes', json=dict(
            previous_questions=[10],
            quiz_category={'type': 'Sports', 'id': 6}
        ))

        payload = json.loads(res.data)
        one_of = [
            {
                "data": {
                    "question": {
                        "answer": "Uruguay",
                        "category": 6,
                        "difficulty": 4,
                        "id": 11,
                        "question": "Which country won the first ever soccer World Cup in 1930?"
                    }
                },
                "message": "OK",
                "status": 200
            }
        ]
        not_of = [
            {
                "data": {
                    "question": {
                        "answer": "Brazil",
                        "category": 6,
                        "difficulty": 3,
                        "id": 10,
                        "question": "Which is the only team to play in every soccer World Cup tournament?"
                    }
                },
                "message": "OK",
                "status": 200
            },
        ]

        self.assertEqual(res.status_code, 200)
        self.assertIn(payload, one_of)
        self.assertNotIn(payload, not_of)

    def test_api_returns_empty_result_on_no_more_questions(self):
        """Test API returns empty result when all questions are already served
            : POST /quizzes
        """
        res = self.client().post('/quizzes', json=dict(
            previous_questions=[10, 11],
            quiz_category={'type': 'Sports', 'id': 6}
        ))

        payload = json.loads(res.data)
        expected = {
            "data": {},
            "message": "OK",
            "status": 200
        }

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload, expected)

    def test_api_returns_questions_of_all_category(self):
        """Test API returns random questions in any category when All categories selected
            : POST /quizzes
        """
        res = self.client().post('/quizzes', json=dict(
            previous_questions=[],
            quiz_category={'id': 0}
        ))

        payload = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(payload['data']['question'])

    def test_fetch_quizzes_using_wrong_path(self):
        """Test making API request to wrong path returns 404 Error
            : POST /quizzes
        """
        WRONG_PATH = '/quiz'
        res = self.client().post(WRONG_PATH, json=dict(
            previous_questions=[],
            quiz_category={'type': 'Sports', 'id': 6}
        ))

        payload = json.loads(res.data)
        expected = {
            'data': {},
            'message': 'Not Found',
            'status': 404,
        }

        self.assertEqual(res.status_code, 404)
        self.assertEqual(payload, expected)

    def test_fetch_quizzes_using_wrong_method(self):
        """Test making API request with wrong HTTP method returns 405 Error
            : PUT /quizzes
        """
        res = self.client().put('/quizzes', json=dict(
            previous_questions=[],
            quiz_category={'type': 'Sports', 'id': 6}
        ))

        payload = json.loads(res.data)
        expected = {
            'data': {},
            'message': 'Method Not Allowed',
            'status': 405,
        }

        self.assertEqual(res.status_code, 405)
        self.assertEqual(payload, expected)

    def test_fetch_quizzes_using_wrong_parameters(self):
        """Test making API request with wrong parameters returns 400 Error
            : POST /quizzes
        """
        WRONG_PARAM = 'Sports'
        res = self.client().post('/quizzes', json=dict(
            previous_questions=[],
            quiz_category=WRONG_PARAM
        ))

        payload = json.loads(res.data)
        expected = {
            'data': {},
            'message': 'Bad Request',
            'status': 400,
        }

        self.assertEqual(res.status_code, 400)
        self.assertEqual(payload, expected)
