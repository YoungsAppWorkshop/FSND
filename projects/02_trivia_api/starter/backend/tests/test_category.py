import json

from tests.test_flaskr import TriviaTestCase


class CategoryTestCase(TriviaTestCase):
    def test_fetch_categories(self):
        """Test handling GET requests for all available categories
            : GET /categories
        """
        res = self.client().get('/categories')

        payload = json.loads(res.data)
        expected = {
            'data': {
                'categories': {
                    '1': "Science",
                    '2': "Art",
                    '3': "Geography",
                    '4': "History",
                    '5': "Entertainment",
                    '6': "Sports",
                },
            },
            'message': 'OK',
            'status': 200,
        }

        self.assertEqual(res.status_code, 200)
        self.assertEqual(payload, expected)

    def test_fetch_categories_using_wrong_path(self):
        """Test making API request to wrong path returns 404 Error
            : GET /categories
        """
        WRONG_PATH = '/category'
        res = self.client().get(WRONG_PATH)

        payload = json.loads(res.data)
        expected = {
            'data': {},
            'message': 'Not Found',
            'status': 404,
        }

        self.assertEqual(res.status_code, 404)
        self.assertEqual(payload, expected)

    def test_fetch_categories_using_wrong_method(self):
        """Test making API request with wrong HTTP method returns 405 Error
            : POST /categories
        """
        res = self.client().post('/categories')

        payload = json.loads(res.data)
        expected = {
            'data': {},
            'message': 'Method Not Allowed',
            'status': 405,
        }

        self.assertEqual(res.status_code, 405)
        self.assertEqual(payload, expected)
