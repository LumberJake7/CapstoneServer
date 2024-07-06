# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class SignupUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    displayname = StringField("Display Name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=128, message='Password must be between 8 and 128 characters long')])
