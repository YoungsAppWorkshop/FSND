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
