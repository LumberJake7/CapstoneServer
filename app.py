from flask import Flask, request, render_template, redirect, flash, session, url_for, jsonify, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db, Menu
from forms import LoginUserForm, SignupUserForm
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import check_password_hash
import requests
import os

def create_app(config_object='config_module.ConfigClass'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///menu"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key') 
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

    toolbar = DebugToolbarExtension(app)
    API_KEY = '0a6d6c9f43cc45f4a8ac20b49d8d36fd'


    connect_db(app)
    #################### Base Functions and HomePage ##############################


    @app.route('/')
    def homepage():
        # Check if user is logged in
        if 'user_id' in session:
            return redirect(url_for('ingredient_search'))  # Redirect to the search ingredients route

        # Normal homepage logic for visitors who are not logged in
        recipe_ids = [795514, 715544, 754183]
        recipe_data = {}

        for recipe_id in recipe_ids:
            recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
            response = requests.get(recipe_url)
            recipe_data[recipe_id] = response.json()
        
        return render_template('home.html', recipe_data=recipe_data)


    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginUserForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            return_user = User.authenticate(username, password)
            
            if return_user:
                flash(f"Hello, you're back {return_user.displayname}")
                session['user_id'] = return_user.id
                session['displayname'] = return_user.displayname
                return redirect('/')
            else:
                form.username.errors.clear()
                form.password.errors.clear()
                form.username.errors.append("Invalid username/password")

        return render_template("login.html", form=form)


    @app.route('/signup', methods=['GET', 'POST'])
    def sign_up():
        form = SignupUserForm()

        if form.validate_on_submit():
            username = form.username.data
            displayname = form.displayname.data
            password = form.password.data

            # Check if the username already exists
            if User.query.filter_by(username=username).first():
                flash('Username taken. Please pick another', 'error')
                return render_template('signup.html', form=form)

            try:
                new_user = User.register(username, displayname, password)
                db.session.add(new_user)
                db.session.commit()

                new_menu = Menu(user_id=new_user.id)
                db.session.add(new_menu)
                db.session.commit()

                session['user_id'] = new_user.id
                session['displayname'] = displayname
                flash('Registration successful!', 'success')
                return redirect('/')
            except IntegrityError:
                db.session.rollback()
                flash('An unexpected error occurred. Please try again.', 'error')
                return render_template('signup.html', form=form)
        else:
            return render_template('signup.html', form=form)



    @app.route("/logout")
    def logout():
        if 'user_id' in session:
            session.pop('user_id')
        flash("Goodbye!")
        return redirect('/')


    ####################User Routes and Functions######################


    @app.route('/users/<int:user_id>', methods=['GET'])
    def profile(user_id):
        user = User.query.get_or_404(user_id)
        menu_items = Menu.query.filter_by(user_id=user_id).all()
        
        recipe_data = []
        for menu_item in menu_items:
            recipe_id = menu_item.recipe_id
            if recipe_id:
                try:
                    recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
                    response = requests.get(recipe_url)
                    if response.status_code == 200:
                        recipe_info = response.json()
                        recipe_data.append(recipe_info)
                    else:
                        app.logger.error(f"Failed to fetch recipe {recipe_id}. Status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    app.logger.error(f"Request exception for recipe {recipe_id}: {e}")
                except ValueError as e:
                    app.logger.error(f"JSON decoding failed for recipe {recipe_id}: {e}")
        
        return render_template('users/profile.html', user=user, recipe_data=recipe_data)

    @app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
    def edit_profile(user_id):
        user = User.query.get_or_404(user_id)
        form = SignupUserForm(obj=user) 
        
        if 'user_id' not in session or session['user_id'] != user_id:
            flash("You are not authorized to edit this profile.", "danger")
            return redirect(url_for('homepage'))
        
        if form.validate_on_submit():
            username = form.username.data
            displayname = form.displayname.data
            password = form.password.data
            
            if not check_password_hash(user.password, password):
                flash("Incorrect password. Please try again.", "danger")
                return redirect(url_for('edit_profile', user_id=user_id))
            
            try:
                user.username = username
                user.displayname = displayname
                session['displayname'] = displayname
                db.session.commit()
                flash("Profile Successfully Updated")
                return redirect(f"/users/{user.id}")
            except Exception as e:
                db.session.rollback()
                flash("An error occurred while updating the profile. Please try again later.", "danger")
                app.logger.error(f"Error updating profile for user {user_id}: {str(e)}")
                return redirect(url_for('edit_profile', user_id=user_id))

        return render_template('users/edit.html', user=user, form=form)

    @app.route('/users/add_to_menu/<int:recipe_id>', methods=['GET', 'POST'])
    def add_or_remove_from_menu(recipe_id):
        if request.method == 'POST':
            
            user_id = session.get('user_id')
            
            if user_id is None:
                abort(401)  # Unauthorized

            existing_menu_item = Menu.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
            if existing_menu_item:
                print('deleted')
                db.session.delete(existing_menu_item)
                db.session.commit()
                flash('Recipe removed from menu successfully!')
            else:
                print('added')
                new_menu_item = Menu(user_id=user_id, recipe_id=recipe_id)
                db.session.add(new_menu_item)
                db.session.commit()
                flash('Recipe added to menu successfully!')

            return redirect(request.referrer or '/')
        else:
            return 'Method not allowed'


    ################ Search Function, Menu Functions, and Recipes ##############################


    @app.route('/search/ingredients', methods=['GET', 'POST'])
    def ingredient_search():
        user_id = session.get('user_id')
        if user_id is None:
            flash("You must login or create an account to see this page")
            return redirect('/login')
        if request.method == 'POST':
            ingredients = [ingredient for ingredient in request.form.getlist('ingredients[]') if ingredient.strip()]
            ignore_pantry = 'true' if request.form.get('ignorePantry') else 'false'
            
            if ingredients:
                ingredients_str = ','.join(ingredients)
                api_url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}&ingredients={ingredients_str}&number=5&ignorePantry={ignore_pantry}'
                
                response = requests.get(api_url)
                results = response.json()
                
                filtered_results = [recipe for recipe in results if recipe['title'] not in ['Beverages', 'Smoothies']]
                
                return render_template('search/ingredients.html', results=filtered_results)
        
        return render_template('search/ingredients.html')

    @app.route('/search/details/<int:recipe_id>', methods=['GET', 'POST'])
    def results(recipe_id):
        user_id = session.get('user_id')
        if user_id is None:
            flash("You must login or create an account to see this page")
            return redirect('/login')
        
        user_menu_ids = [menu.recipe_id for menu in Menu.query.filter_by(user_id=user_id).all()]
        image_request = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
        summary_request = f'https://api.spoonacular.com/recipes/{recipe_id}/summary?apiKey={API_KEY}'
        instruction_request = f'https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={API_KEY}'

        sum_response = requests.get(summary_request)
        inst_response = requests.get(instruction_request)
        image_response = requests.get(image_request)
        
        if sum_response.status_code == 200 and inst_response.status_code == 200 and image_response.status_code == 200:
            summary = sum_response.json()
            summary_text = summary['summary'].split('With a spoonacular score')[0].strip()
            summary['summary'] = summary_text
            instructions = inst_response.json()
            image_data = image_response.json()

            ingredient_set = set()
            equipment_set = set()
            for instruction in instructions:
                for step in instruction['steps']:
                    for ingredient in step['ingredients']:
                        ingredient_set.add(ingredient['name'].capitalize())
                    for equipment in step['equipment']:
                        equipment_set.add(equipment['name'].capitalize())

            return render_template("recipeDetails.html", instructions=instructions, summary=summary, image=image_data, user_menu_ids=user_menu_ids, ingredient_set=ingredient_set, equipment_set=equipment_set)
        else:
            return "Failed to retrieve recipe details", 404

    return app



if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)