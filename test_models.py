import unittest
from flask import Flask
from app import db, User, Menu

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_model(self):
        with self.app.app_context():
            user = User(username='test_user', displayname='Test User', password='password')
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(username='test_user').first()

            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.displayname, 'Test User')

    def test_menu_model(self):
        with self.app.app_context():
            user = User(username='test_user', displayname='Test User', password='password')
            db.session.add(user)
            db.session.commit()

            menu_item = Menu(user_id=user.id, recipe_id=123)
            db.session.add(menu_item)
            db.session.commit()

            retrieved_menu_item = Menu.query.first()

            self.assertIsNotNone(retrieved_menu_item)
            self.assertEqual(retrieved_menu_item.user_id, user.id)
            self.assertEqual(retrieved_menu_item.recipe_id, 123)

if __name__ == '__main__':
    unittest.main()
