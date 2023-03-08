from app import db


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.DECIMAL(4, 2), nullable=False, default=0)
    items_sold = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(3000), nullable=False)
    slogan = db.Column(db.String(500), nullable=False)
    payment_account = db.Column(db.String(255), nullable=False)
    logo_dir = db.Column(
        db.String(255), nullable=False, default="shop_logos/default_shop.jpg"
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(
        self,
        name,
        city,
        rating,
        items_sold,
        description,
        slogan,
        payment_account,
        logo_dir,
        user_id,
    ):
        self.name = name
        self.city = city
        self.rating = rating
        self.items_sold = items_sold
        self.description = description
        self.slogan = slogan
        self.payment_account = payment_account
        self.logo_dir = logo_dir
        self.user_id = user_id
