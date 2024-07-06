from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
import os
import requests
from models import connect_db, db

def create_app(config_object='config_module.ConfigClass'):
    app = Flask(__name__)

    # Load environment variables
    database_uri = os.environ.get('DATABASE_URI', 'postgresql://localhost/defaultdb')
    api_key = os.environ.get('SPOONACULAR_API_KEY', 'default_api_key')
    secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config['SECRET_KEY'] = secret_key
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

    toolbar = DebugToolbarExtension(app)
    connect_db(app)

    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from routes.users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from routes.search import search as search_blueprint
    app.register_blueprint(search_blueprint)

    @app.route('/')
    def homepage():
        recipe_ids = [795614, 715544, 754183]
        recipe_data = {}

        for recipe_id in recipe_ids:
            recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}'
            response = requests.get(recipe_url)
            recipe_data[recipe_id] = response.json()

        return render_template('home.html', recipe_data=recipe_data)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
