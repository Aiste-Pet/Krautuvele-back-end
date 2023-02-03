from app import db


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_line = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.Integer)
    country = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, address_line, city, postal_code, country, user_id):
        self.address_line = address_line
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.user_id = user_id
