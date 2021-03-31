from decimal import Decimal
from app.extensions import db, login_manager
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from currency_symbols import CurrencySymbols


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(6), default='member')
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')
    tags = db.relationship('Tag', backref='user', lazy='dynamic')
    modes = db.relationship('PaymentMode', backref='user', lazy='dynamic')
    estimates = db.relationship('Budget', backref='user', lazy='dynamic')
    limit = db.Column(db.Integer, default=1000)
    ccy_iso = db.Column(db.String(3), nullable=False,
                        default=Config.DEFAULT_CURRENCY)
    ccy_override = db.Column(db.String(6))
    allow_decimals = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.add_default_modes()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def currency(self):

        if self.ccy_override:
            return self.ccy_override

        return CurrencySymbols.get_symbol(self.ccy_iso)

    def add_default_modes(self):

        p1 = PaymentMode(mode='Cash')
        p2 = PaymentMode(mode='Netbanking')

        self.modes = [p1, p2]

    def __repr__(self):
        return f'<User: {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


tags = db.Table(
    'expense_tags',
    db.Column('expense_id', db.Integer, db.ForeignKey('expenses.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(128), nullable=False)
    amount_str = db.Column(db.String(12), nullable=False)
    date = db.Column(db.Date, index=True)
    mode_id = db.Column(db.Integer, db.ForeignKey('modes.id'))
    comments = db.Column(db.String(512))
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('expenses', lazy='dynamic')
    )
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, onupdate=db.func.now(),
                           default=db.func.now())

    @property
    def amount(self):

        if current_user.allow_decimals:
            return Decimal(self.amount_str)

        return round(Decimal(self.amount_str), 0)

    @amount.setter
    def amount(self, value):

        value = round(Decimal(value), 2)
        self.amount_str = str(value)

    def __repr__(self):
        return f'<Expense: {self.amount}>'


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tagname = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Tag: {self.tagname}>'


class PaymentMode(db.Model):
    __tablename__ = 'modes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    expenses = db.relationship(Expense, backref='payment_mode', lazy='dynamic')
    mode = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Mode: {self.mode}>'


class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item = db.Column(db.String(64), nullable=False)
    estimate = db.Column(db.Integer)
    due = db.Column(db.String(64))
    comments = db.Column(db.String(512))

    def __repr__(self):
        return f'<Budget-item: {self.item}>'
