from app import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(800), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    product_category_id = db.Column(db.Integer, db.ForeignKey("product_category.id"))
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))

    def __init__(self, name, price, description, product_category_id, shop_id):
        self.name = name
        self.price = price
        self.description = description
        self.product_category_id = product_category_id
        self.shop_id = shop_id
