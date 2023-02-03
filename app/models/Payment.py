from app import db


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)

    def __init__(self, amount, status, type):
        self.amount = amount
        self.status = status
        self.type = type
