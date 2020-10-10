from tests.test_flaskr import TriviaTestCase


class QuizTestCase(TriviaTestCase):
    def test_play_quiz(self):
        """Test handling POST requests for playing quiz game
            : POST /quizzes
        """
        res = self.client().post('/quizzes', json=dict(
            previous_questions=[],
            quiz_category={"type": "Science", "id": "1"},
        ))

        self.assertEqual(res.status_code, 200)
