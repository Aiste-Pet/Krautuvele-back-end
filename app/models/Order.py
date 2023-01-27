from app import db
from datetime import datetime


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    payment_id = db.Column(db.Integer, db.ForeignKey("payment.id"))
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, user_id, payment_id, total, created_at):
        self.user_id = user_id
        self.payment_id = payment_id
        self.total = total
        self.created_at = created_at
