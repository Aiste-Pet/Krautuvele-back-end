from app import db


class Product_property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    def __init__(self, name, value, product_id):
        self.name = name
        self.value = value
        self.product_id = product_id
