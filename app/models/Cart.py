from app import db
from datetime import datetime


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    def __init__(self, quantity, created_at, user_id, product_id):
        self.quantity = quantity
        self.created_at = created_at
        self.user_id = user_id
        self.product_id = product_id
