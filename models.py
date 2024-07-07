from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)  # Increase the length to 60
    displayname = db.Column(db.String(100), nullable=False)
    menu = db.relationship('Menu', backref='user', lazy=True)

    @classmethod
    def register(cls, username, displayname, password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = cls(username=username, password=hashed_pwd, displayname=displayname)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
