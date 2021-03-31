from datetime import datetime
from collections import defaultdict

from flask_login import current_user

from app.models import Expense, PaymentMode
from app.extensions import db


def get_context(year):

    expenses = Expense.query \
        .filter(Expense.user_id == current_user.id,
                db.extract('year', Expense.date) == year) \
        .order_by(Expense.date)

    utcnow = datetime.utcnow()
    curr_year = utcnow.year
    curr_month = utcnow.month
    curr_month_full = utcnow.strftime('%B')
    curr_month_abbr = utcnow.strftime('%b')

    ctx = {
        'year': year,
        'month': curr_month_full,
        'month-totals': get_month_totals(expenses),
        'current-month-expenses': get_curr_mon_exp(curr_month, expenses),
        'limit': current_user.limit,
        'scatter': get_outliers(expenses),
        'payment-mode': get_expenses_by_payment_mode(expenses)
    }

    ctx['month-total'] = ctx['month-totals'][curr_month_abbr]
    ctx['num-of-months'] = len(ctx['month-totals'])

    if year == curr_year:
        ctx['ytd'] = sum(ctx['month-totals'].values())
        ctx['mtd'] = list(ctx['month-totals'].values())[-1]
    else:
        ctx['year-total'] = sum(ctx['month-totals'].values())

    return ctx


def get_month_totals(expenses):

    month_totals = defaultdict(int)

    for e in expenses:
        month_totals[e.date.strftime('%b')] += e.amount

    return month_totals


def get_curr_mon_exp(mon, expenses):

    curr_mon_exp = expenses.filter(db.extract('month', Expense.date) == mon)

    ret = []

    for exp in curr_mon_exp:
        ret.append((exp.description, exp.amount))

    return ret


def get_outliers(expenses):

    limit = current_user.limit
    outliers = []

    for e in expenses:
        if e.amount > limit:
            outliers.append((e.date.strftime('%b'),
                             e.date.strftime('%b %d'),
                             e.amount))

    return outliers


def get_expenses_by_payment_mode(expenses):

    by_mode = defaultdict(int)

    for e in expenses:
        by_mode[e.mode_id] += e.amount

    return [(PaymentMode.query.get(k).mode, v) for k, v in by_mode.items()]
