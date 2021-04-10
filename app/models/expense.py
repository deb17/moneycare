from decimal import Decimal

from flask_login import current_user
from sqlalchemy import cast, Numeric
from sqlalchemy.ext.hybrid import hybrid_property

from flask_whooshalchemy import Searcher
from whoosh.analysis import StemmingAnalyzer
from whoosh.query import FuzzyTerm
from whoosh.qparser import OrGroup, AndGroup, MultifieldParser

from app.extensions import db
from app.models import Tag

tags = db.Table(
    'expense_tags',
    db.Column('expense_id', db.Integer, db.ForeignKey('expenses.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class CustomFuzzyTerm(FuzzyTerm):
    def __init__(self, fieldname, text, boost=1.0, maxdist=2,
                 prefixlength=1, constantscore=True):
        super().__init__(fieldname, text, boost,
                         maxdist, prefixlength, constantscore)


def call_function(self, query, limit=None, fields=None, or_=False):
    if fields is None:
        fields = self.fields
    group = OrGroup if or_ else AndGroup
    parser = MultifieldParser(fields, self.index.schema, group=group,
                              termclass=CustomFuzzyTerm)
    results = []
    with self.searcher() as searcher:
        for doc in searcher.search(parser.parse(query), limit=limit):
            results.append(doc[self.pk])
    return results


Searcher.__call__ = call_function


class Expense(db.Model):
    __tablename__ = 'expenses'
    __searchable__ = ['description', 'comments']
    __analyzer__ = StemmingAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(64), nullable=False)
    amount_str = db.Column(db.String(12), nullable=False)
    date = db.Column(db.Date, index=True)
    mode_id = db.Column(db.Integer, db.ForeignKey('modes.id'))
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))
    comments = db.Column(db.String(512))
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('expenses', lazy='dynamic')
    )
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, onupdate=db.func.now(),
                           default=db.func.now())

    @hybrid_property
    def amount(self):

        if current_user.allow_decimals:
            return Decimal(self.amount_str)

        return round(Decimal(self.amount_str), 0)

    @amount.expression
    def amount(cls):

        if current_user.allow_decimals:
            return cast(cls.amount_str, Numeric(12, 2))
        return cast(cls.amount_str, Numeric(12, 0))

    @amount.setter
    def amount(self, value):

        value = round(Decimal(value), 2)
        self.amount_str = str(value)

    @classmethod
    def amount_num(cls, amount_str):

        if current_user.allow_decimals:
            return Decimal(amount_str)

        return round(Decimal(amount_str), 0)

    def set_tags(self, taglist):

        for tagname in taglist.split(','):
            if tagname:
                tag = Tag.query.filter_by(
                    user_id=self.user_id, tagname=tagname.lower()).first()
                if not tag:
                    tag = Tag(user_id=self.user_id, tagname=tagname.lower())
                self.tags.append(tag)

    def __repr__(self):
        return f'<Expense: {self.amount}>'
