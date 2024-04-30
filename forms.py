from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class LoginUserForm(FlaskForm):
    username = StringField("Username", validators =[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class SignupUserForm(FlaskForm):
    username = StringField("Username", validators =[InputRequired()])
    displayname = StringField("Display Name", validators =[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

