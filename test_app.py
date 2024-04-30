import unittest
from unittest.mock import patch, MagicMock
from flask import session, url_for
from app import create_app
from sqlalchemy.exc import IntegrityError

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('your_test_config_here')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    @patch('app.User.authenticate')
    def test_successful_login(self, mock_authenticate):
        mock_authenticate.return_value = True
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch('app.User.authenticate')
    def test_failed_login(self, mock_authenticate):
        mock_authenticate.return_value = False
        response = self.client.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    @patch('app.db.session.add', MagicMock())
    @patch('app.db.session.commit', MagicMock())
    def test_successful_signup(self):
        with patch('app.User.register') as mock_register:
            mock_register.return_value = MagicMock(id=123, displayname='testuser')
            response = self.client.post('/signup', data={
                'username': 'newuser',
                'displayname': 'New User',
                'password': 'newpassword'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    @patch('app.db.session.add', MagicMock())
    def test_signup_with_taken_username(self):
        with patch('app.db.session.commit') as mock_commit:
            mock_commit.side_effect = IntegrityError('', '', '')
            response = self.client.post('/signup', data={
                'username': 'takenuser',
                'displayname': 'Taken User',
                'password': 'password'
            })
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            response = c.get('/logout', follow_redirects=True)
            self.assertNotIn('user_id', session)
            self.assertTrue(response.request.path == '/')

    @patch('requests.get')
    def test_user_profile(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'some': 'data'}
        user_id = 1  
        response = self.client.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)

    @patch('app.User.query')
    def test_edit_profile_not_logged_in(self, mock_query):
        mock_query.get_or_404.return_value = MagicMock(id=1)
        response = self.client.post('/users/1/edit', data={}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    @patch('app.User.query')
    @patch('app.check_password_hash', return_value=True)
    def test_edit_profile_success_redirect(self, mock_check_password_hash, mock_query):
        user = MagicMock(id=1, username="testuser", displayname="Test User")
        mock_query.get_or_404.return_value = user
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            response = c.post('/users/1/edit', data={
                'username': 'newusername',
                'displayname': 'New Displayname',
                'password': 'correctpassword'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('id="user_form"', response.get_data(as_text=True))

    @patch('app.Menu.query')
    def test_add_to_menu_unauthorized(self, mock_query):
        response = self.client.post('/users/add_to_menu/123', data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    
    @patch('app.requests.get')
    def test_ingredient_search_not_logged_in(self, mock_get):
        response = self.client.get('/search/ingredients', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue("/login" in response.location)

    @patch('app.requests.get')
    def test_ingredient_search_with_results(self, mock_get):
        # Mock the user login
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
            
            # Mock the external API response
            mock_get.return_value.json.return_value = [
                {"title": "Test Recipe", "id": 123, "image": "test_image.jpg"}
            ]
            mock_get.return_value.status_code = 200

            response = self.client.post('/search/ingredients', data={
                'ingredients[]': ['chicken', 'rice'],
                'ignorePantry': 'true'
            })

            self.assertEqual(response.status_code, 200)
            self.assertIn("Test Recipe", response.get_data(as_text=True))

    @patch('app.requests.get')
    def test_results_not_logged_in(self, mock_get):
        response = self.client.get('/search/details/123', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue("/login" in response.location)

    @patch('app.requests.get')
    def test_results_with_valid_recipe(self, mock_get):
        mock_summary_response = MagicMock(status_code=200, json=lambda: {"summary": "Test Summary"})
        mock_instructions_response = MagicMock(status_code=200, json=lambda: [{"steps": [{"ingredients": [{"name": "chicken"}], "equipment": [{"name": "oven"}]}]}])
        mock_image_response = MagicMock(status_code=200, json=lambda: {"image": "test_image.jpg"})
        mock_get.side_effect = [mock_summary_response, mock_instructions_response, mock_image_response]

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

            response = c.get('/search/details/123')

            self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
    unittest.main()
