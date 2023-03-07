from app import db


class Cart_items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, cart_id, product_id, quantity, price):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
