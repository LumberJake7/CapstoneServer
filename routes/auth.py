from flask import Blueprint, render_template, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from models import User, db, Menu
from forms import LoginUserForm, SignupUserForm

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        return_user = User.authenticate(username, password)
        
        if return_user:
            flash(f"Hello, you're back {return_user.displayname}", 'success')
            session['user_id'] = return_user.id
            session['displayname'] = return_user.displayname
            return redirect('/')
        else:
            form.username.errors.clear()
            form.password.errors.clear()
            form.username.errors.append("Invalid username/password")

    return render_template("login.html", form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignupUserForm()

    if form.validate_on_submit():
        username = form.username.data
        displayname = form.displayname.data
        password = form.password.data

        user = User.register(username, displayname, password)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Account created successfully!', 'success')
            session['user_id'] = user.id
            
            # Add a sample recipe to the user's menu (assuming 12345 is a valid recipe_id)
            sample_recipe_id = 12345
            if sample_recipe_id:  # Ensure the recipe_id is valid
                menu_item = Menu(user_id=user.id, recipe_id=sample_recipe_id)
                db.session.add(menu_item)
                db.session.commit()
            
            return redirect(url_for('search.ingredient_search'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Username already exists. Please choose a different one.', 'danger')
            form.username.errors.append("Username already exists")
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'danger')
            print(f"Error: {e}")

    return render_template('signup.html', form=form)

@auth.route("/logout")
def logout():
    session.clear()
    flash("Goodbye!", 'info')
    return redirect('/')

