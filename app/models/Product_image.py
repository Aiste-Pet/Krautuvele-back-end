from app import db


class Product_image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    public_dir = db.Column(
        db.String(255), nullable=False, default="default_product.jpg"
    )
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    def __init__(self, type, public_dir, product_id):
        self.type = type
        self.public_dir = public_dir
        self.product_id = product_id
