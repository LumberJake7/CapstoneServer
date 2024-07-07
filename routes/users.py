from flask import Blueprint, render_template, redirect, url_for, session, request, flash, abort, current_app
from models import User, db, Menu
from forms import SignupUserForm
from flask_bcrypt import check_password_hash
import requests

users = Blueprint('users', __name__)

@users.route('/users/<int:user_id>', methods=['GET'])
def profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("You are not authorized to view this profile.", "danger")
        return redirect(url_for('homepage'))
    
    user = User.query.get_or_404(user_id)
    menu_items = Menu.query.filter_by(user_id=user_id).all()
    
    recipe_data = []
    for menu_item in menu_items:
        recipe_id = menu_item.recipe_id
        if recipe_id:
            try:
                api_key = current_app.config['API_KEY']
                recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}'
                response = requests.get(recipe_url)
                if response.status_code == 200:
                    recipe_info = response.json()
                    recipe_data.append(recipe_info)
                else:
                    users.logger.error(f"Failed to fetch recipe {recipe_id}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                users.logger.error(f"Request exception for recipe {recipe_id}: {e}")
            except ValueError as e:
                users.logger.error(f"JSON decoding failed for recipe {recipe_id}: {e}")
    
    return render_template('users/profile.html', user=user, recipe_data=recipe_data)

@users.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("You are not authorized to edit this profile.", "danger")
        return redirect(url_for('homepage'))
    
    user = User.query.get_or_404(user_id)
    form = SignupUserForm(obj=user) 
    
    if form.validate_on_submit():
        username = form.username.data
        displayname = form.displayname.data
        password = form.password.data
        
        if not check_password_hash(user.password, password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for('users.edit_profile', user_id=user_id))
        
        try:
            user.username = username
            user.displayname = displayname
            session['displayname'] = displayname
            db.session.commit()
            flash("Profile Successfully Updated")
            return redirect(url_for('users.profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the profile. Please try again later.", "danger")
            users.logger.error(f"Error updating profile for user {user_id}: {str(e)}")
            return redirect(url_for('users.edit_profile', user_id=user.id))

    return render_template('users/edit.html', user=user, form=form)

@users.route('/users/add_to_menu/<int:recipe_id>', methods=['POST'])
def add_or_remove_from_menu(recipe_id):
    if 'user_id' not in session:
        abort(401)  # Unauthorized
    
    user_id = session['user_id']

    existing_menu_item = Menu.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing_menu_item:
        db.session.delete(existing_menu_item)
        db.session.commit()
        flash('Recipe removed from menu successfully!')
    else:
        new_menu_item = Menu(user_id=user_id, recipe_id=recipe_id)
        db.session.add(new_menu_item)
        db.session.commit()
        flash('Recipe added to menu successfully!')

    return redirect(request.referrer or '/')
