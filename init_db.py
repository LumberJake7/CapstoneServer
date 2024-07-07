from app import create_app
from models import db

app = create_app()

with app.app_context():
    db.drop_all()  # Be careful with this in production
    db.create_all()

    print("Database tables created successfully")
