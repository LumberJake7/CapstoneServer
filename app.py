from flask import Flask, render_template, jsonify, session, redirect, url_for, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate  # Import Migrate
import os
import requests
from models import connect_db, db, User

# Global variable to cache recipe data
cached_data = None

def create_app(config_object='config_module.ConfigClass'):
    app = Flask(__name__)
    
    # Configuration settings
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = os.getenv('SQLALCHEMY_ECHO', 'False') == 'True'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')
    app.config['API_KEY'] = os.getenv('API_KEY') 
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

    # Extensions
    bcrypt = Bcrypt(app)
    
    # Connect database
    connect_db(app)
    
    # Initialize migration
    migrate = Migrate(app, db)

    # Register blueprints
    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from routes.users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    from routes.search import search as search_blueprint
    app.register_blueprint(search_blueprint, url_prefix='/search')

    # Define route for homepage
    @app.route('/')
    def homepage():
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        return render_template('home.html', user=user)

    # API route to get recipes
    @app.route('/api/recipes')
    def get_recipes():
        global cached_data
        if cached_data is None:
            recipe_ids = [795614, 715544, 754183]
            recipe_data = {}

            for recipe_id in recipe_ids:
                recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={current_app.config["API_KEY"]}'
                response = requests.get(recipe_url)
                recipe_data[recipe_id] = response.json()
            
            cached_data = recipe_data
        
        return jsonify(cached_data)

    @app.context_processor
    def inject_user():
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        return dict(user=user)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=False)
