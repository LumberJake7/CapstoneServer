from flask import Blueprint, render_template, redirect, url_for, session, request, flash, abort
from models import User, db, Menu
from forms import EditProfileForm
from flask_bcrypt import check_password_hash
import requests
import os

users = Blueprint('users', __name__, template_folder='templates/users')

API_KEY = os.getenv('API_KEY')

@users.route('/<int:user_id>', methods=['GET'])
def profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("You are not authorized to view this profile.", "danger")
        return redirect(url_for('homepage'))
    
    user = User.query.get_or_404(user_id)
    menu_items = Menu.query.filter_by(user_id=user_id).all()
    
    recipe_data = []
    user_menu_ids = []
    for menu_item in menu_items:
        recipe_id = menu_item.recipe_id
        user_menu_ids.append(recipe_id)
        if recipe_id:
            try:
                recipe_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
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
    
    return render_template('users/profile.html', user=user, recipe_data=recipe_data, user_menu_ids=user_menu_ids)

@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("You are not authorized to edit this profile.", "danger")
        return redirect(url_for('homepage'))
    
    user = User.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)
    
    if form.validate_on_submit():
        print("Form validated")
        username = form.username.data
        displayname = form.displayname.data
        password = form.password.data

        print(f"Username: {username}")
        print(f"Display Name: {displayname}")
        print(f"Password: {password}")

        # Verify the password
        if not check_password_hash(user.password, password):
            print("Password check failed")
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for('users.edit_profile', user_id=user_id))
        
        try:
            user.username = username
            user.displayname = displayname
            session['displayname'] = displayname
            db.session.commit()
            print("Profile updated")
            flash("Profile Successfully Updated", "success")
            return redirect(url_for('users.profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            print(f"Error during update: {e}")
            flash("An error occurred while updating the profile. Please try again later.", "danger")
            return redirect(url_for('users.edit_profile', user_id=user.id))
    else:
        print("Form not valid")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in the {getattr(form, field).label.text} field - {error}")

    return render_template('users/edit.html', user=user, form=form)


@users.route('/add_to_menu/<int:recipe_id>', methods=['POST'])
def add_or_remove_from_menu(recipe_id):
    if 'user_id' not in session:
        abort(401)  # Unauthorized
    
    user_id = session['user_id']

    existing_menu_item = Menu.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing_menu_item:
        db.session.delete(existing_menu_item)
        db.session.commit()
        flash('Recipe removed from menu successfully!', 'success')
    else:
        new_menu_item = Menu(user_id=user_id, recipe_id=recipe_id)
        db.session.add(new_menu_item)
        db.session.commit()
        flash('Recipe added to menu successfully!', 'success')

    return redirect(request.referrer or '/')
