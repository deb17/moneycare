from app.extensions import db


class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    expenses = db.relationship('Expense', backref='estimate', lazy='dynamic')
    item = db.Column(db.String(64), nullable=False)
    estimate = db.Column(db.Integer)
    due = db.Column(db.String(64))
    comments = db.Column(db.String(512))
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Budget-item: {self.item}>'
