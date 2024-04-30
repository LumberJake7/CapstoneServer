import unittest
from app import app
from flask import session
from flask.testing import FlaskClient
from forms import LoginUserForm, SignupUserForm

class TestForms(unittest.TestCase):
    def setUp(self):
        app.config['SECRET_KEY'] = 'test_secret_key'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_login_form(self):
        with self.client as c:
            response = c.post('/login', data=dict(username='testuser', password='password'), follow_redirects=True)
            form = LoginUserForm()
            self.assertTrue(form.validate_on_submit())

    def test_signup_form(self):
        with self.client as c:
            response = c.post('/signup', data=dict(username='testuser', displayname='Test User', password='password'), follow_redirects=True)
            form = SignupUserForm()
            self.assertTrue(form.validate_on_submit())

if __name__ == '__main__':
    unittest.main()
