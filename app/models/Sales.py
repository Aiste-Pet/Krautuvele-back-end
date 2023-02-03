from app import db


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))

    def __init__(self, shop_id, order_id):
        self.shop_id = shop_id
        self.order_id = order_id
