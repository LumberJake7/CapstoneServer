# routes/auth.py

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

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username taken. Please pick another', 'signup')
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
            flash('An unexpected error occurred. Please try again.', 'signup')
            return render_template('signup.html', form=form)
    else:
        return render_template('signup.html', form=form)


@auth.route("/logout")
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    flash("Goodbye!", 'info')
    return redirect('/')
