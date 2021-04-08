from app.extensions import db


class PaymentMode(db.Model):
    __tablename__ = 'modes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    expenses = db.relationship(
        'Expense',
        backref='payment_mode',
        lazy='dynamic'
    )
    mode = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Mode: {self.mode}>'
