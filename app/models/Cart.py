from app import db
from datetime import datetime


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, created_at, user_id):
        self.created_at = created_at
        self.user_id = user_id
