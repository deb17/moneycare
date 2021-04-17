import datetime
from decimal import Decimal

from flask import current_app, session
from flask_login import current_user
from sqlalchemy import case

from app.extensions import db
from app.models import Expense, Tag


def base_query():

    q1 = Expense.query.filter_by(user_id=current_user.id)

    return q1


def filter_year(form):

    q1 = base_query()

    year = int(form.year.data) if form.year.data else None
    if year:
        q2 = q1.filter(db.extract('year', Expense.date) == year)
    else:
        q2 = q1

    return q2


def filter_month(form):

    q2 = filter_year(form)

    months = form.month.data
    if months:
        q3 = q2.filter(db.extract('month', Expense.date).in_(months))
    else:
        q3 = q2

    return q3


def filter_exact_date(form):

    q3 = filter_month(form)

    if form.exact_date.data:
        q4 = q3.filter(Expense.date == form.exact_date.data)
    else:
        q4 = q3

    return q4


def filter_from_to_dates(form):

    q4 = filter_exact_date(form)

    if form.from_date.data:
        q4 = q4.filter(Expense.date >= form.from_date.data)

    if form.to_date.data:
        q5 = q4.filter(Expense.date <= form.to_date.data)
    else:
        q5 = q4

    return q5


def filter_amount(form):

    q5 = filter_from_to_dates(form)

    if form.amount.data:
        expr = get_expression(form.amt_cond.data, form.amount.data)
        q6 = q5.filter(expr)
    else:
        q6 = q5

    return q6


def get_expression(cond, amt):

    if cond == '==':
        expr = Expense.amount == amt
    elif cond == '>':
        expr = Expense.amount > amt
    elif cond == '<':
        expr = Expense.amount < amt
    elif cond == '>=':
        expr = Expense.amount >= amt
    elif cond == '<=':
        expr = Expense.amount <= amt

    return expr


def filter_amt_min_max(form):

    q6 = filter_amount(form)

    if form.amt_min.data:
        q6 = q6.filter(Expense.amount >= form.amt_min.data)

    if form.amt_max.data:
        q7 = q6.filter(Expense.amount <= form.amt_max.data)
    else:
        q7 = q6

    return q7


def filter_payment_modes(form):

    q7 = filter_amt_min_max(form)

    modes = form.payment_modes.data
    if modes:
        q8 = q7.filter(Expense.mode_id.in_(modes))
    else:
        q8 = q7

    return q8


def filter_tags(form):

    q8 = filter_payment_modes(form)

    q9 = q8
    if form.tags.data:
        tags = [Tag.query.get(id) for id in form.tags.data]
        for tag in tags:
            q9 = q9.filter(Expense.tags.contains(tag))

    return q9


def escape(s):

    return s.replace('/', '//').replace('%', '/%').replace('_', '/_')


def filter_description(form):

    q9 = filter_tags(form)

    if form.text.data:
        if form.simple_search.data:
            search_for = '%' + escape(form.text.data) + '%'
            q10 = q9.filter(db.or_(
                Expense.description.ilike(search_for, escape='/'),
                Expense.comments.ilike(search_for, escape='/')
            )).order_by(Expense.date.desc())
        else:
            exp_objects = q9.search(form.text.data, limit=50).all()
            # Following code is needed because the search method does not
            # support pagination. Also the whoosh results order needs to be
            # preserved.
            exp_ids = []
            for exp in exp_objects:
                exp_ids.append(exp.id)
            if exp_ids:
                ordering = case(
                    {id: index for index, id in enumerate(exp_ids)},
                    value=Expense.id
                )
            else:
                ordering = None
            q10 = Expense.query.filter(Expense.id.in_(exp_ids)) \
                .order_by(ordering)
    else:
        q10 = q9.order_by(Expense.date.desc())

    return q10


def search_main(form, page):

    q10 = filter_description(form)

    result = q10.paginate(page, current_app.config['SEARCH_ITEMS_PER_PAGE'],
                          False)
    total = 0
    for exp in q10:
        total += exp.amount

    return result, total


def to_session(form):

    d = {}

    for k, v in form.data.items():
        if v:
            if isinstance(v, (Decimal, datetime.date)):
                v = str(v)
            d[k] = v
    session['search-data'] = d


def from_session():

    form_data = session['search-data']

    for k, v in form_data.items():
        if k in ('amount', 'amt_min', 'amt_max'):
            form_data[k] = Decimal(v)
        if k in ('exact_date', 'from_date', 'to_date'):
            form_data[k] = datetime.date.fromisoformat(v)

    return form_data
