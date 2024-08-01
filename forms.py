from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    displayname = StringField('Display Name', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    displayname = StringField('Display Name', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Edit this user!')