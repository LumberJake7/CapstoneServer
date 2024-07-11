from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import os
import requests
from models import connect_db, db

# Load environment variables from .env if present (mainly for local development)
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()

cached_data = None

def create_app(config_object='config_module.ConfigClass'):
    app = Flask(__name__)

    # Get environment variables
    database_uri = os.environ.get('DATABASE_URL', 'postgresql://localhost/defaultdb')
    api_key = os.environ.get('API_KEY', 'default_api_key')
    secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() in ['true', '1', 'yes']
    app.config['SECRET_KEY'] = secret_key
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['API_KEY'] = api_key  # Store the API key in app config

    connect_db(app)

    # Import and register blueprints
    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from routes.users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    from routes.search import search as search_blueprint
    app.register_blueprint(search_blueprint)

    @app.route('/')
    def homepage():
        return render_template('home.html')

    @app.route('/api/recipes')
    def get_recipes():
        global cached_data
        if cached_data is None:
            recipe_ids = [795614, 715544, 754183]
            recipe_data = {}

            api_key = app.config['API_KEY']
            for recipe_id in recipe_ids:
                recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}'
                response = requests.get(recipe_url)
                if response.status_code == 200:
                    recipe_data[recipe_id] = response.json()
                else:
                    recipe_data[recipe_id] = {'error': f"Failed to fetch recipe {recipe_id}"}

            cached_data = recipe_data
        
        return jsonify(cached_data)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
