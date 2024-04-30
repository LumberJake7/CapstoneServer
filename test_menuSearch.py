import unittest
from unittest.mock import patch, MagicMock
from app import app, API_KEY

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    @patch('app.session', {'user_id': 123})
    @patch('app.requests.get')
    def test_ingredient_search_authenticated(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'title': 'Recipe 1', 'other_key': 'value'},
            {'title': 'Recipe 2', 'other_key': 'value'},
        ]
        response = self.client.post('/search/ingredients', data={'ingredients[]': ['ingredient1', 'ingredient2']})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe 1', response.data)
        self.assertIn(b'Recipe 2', response.data)

    @patch('app.session', {})
    def test_ingredient_search_unauthenticated(self):
        response = self.client.post('/search/ingredients')
        self.assertEqual(response.status_code, 302)

    @patch('app.session', {})
    def test_results_unauthenticated(self):
        response = self.client.get('/search/details/123')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
