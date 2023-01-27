from app import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    picture_dir = db.Column(
        db.String(255), nullable=False, default="default_profile.jpg"
    )

    def __init__(
        self, email, password, first_name, last_name, phone, created_at, picture_dir
    ):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.created_at = created_at
        self.picture_dir = picture_dir
