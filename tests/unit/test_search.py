import datetime

from app.blueprints.search.forms import SearchForm
from app.blueprints.search import utils
from app.blueprints.search.utils import (
    filter_description,
    filter_tags,
    filter_payment_modes,
    filter_amt_min_max,
    filter_amount,
    filter_from_to_dates,
    filter_exact_date,
    filter_month,
    filter_year
)
from app.models import Expense

utils.base_query = lambda: Expense.query.filter_by(user_id=1)


def test_search_description_without_whoosh(db_with_books):

    data = {
        'year': '2021',
        'text': 'book',
        'simple_search': True
    }
    form = SearchForm(data=data)

    retval = filter_description(form)
    assert retval.count() == 2

    books = retval.all()
    assert books[0].description == 'Rest api'
    assert books[1].description == 'Flask cookbook'


def test_search_description_with_whoosh(db_with_books):

    data = {
        'year': '2021',
        'text': 'book'
    }
    form = SearchForm(data=data)

    retval = filter_description(form)
    assert retval.count() == 1

    book = retval.first()
    assert book.comments == 'Book on Rest api.'


def test_fuzzy_search_with_whoosh(db_with_books):

    data = {
        'year': '2021',
        'text': 'boek'
    }
    form = SearchForm(data=data)

    retval = filter_description(form)
    assert retval.count() == 1

    book = retval.first()
    assert book.comments == 'Book on Rest api.'


def test_search_with_whoosh_no_match(db_with_books):

    data = {
        'year': '2021',
        'text': 'cook'
    }
    form = SearchForm(data=data)

    retval = filter_description(form)
    assert retval.count() == 0


def test_search_by_tags(db_with_expense_tags):

    data = {
        'year': '2021',
        'tags': [1, 3]
    }
    form = SearchForm(data=data)

    retval = filter_tags(form)
    expenses = retval.all()
    assert len(expenses) == 1
    assert expenses[0].description == 'Item 3'


def test_search_by_payment_mode(db_with_expenses):

    data = {
        'year': '2021',
        'payment_modes': [1, 2]
    }
    form = SearchForm(data=data)

    retval = filter_payment_modes(form)

    assert retval.count() == 15


def test_search_by_amount_limits(db_with_expense_amounts):

    data = {
        'year': '2021',
        'amt_min': '200',
        'amt_max': '375'
    }
    form = SearchForm(data=data)

    retval = filter_amt_min_max(form)

    assert retval.count() == 3
    for i, exp in enumerate(retval):
        assert exp.description == f'Item {i+2}'


def test_search_by_amount_cond(db_with_expense_amounts):

    data = {
        'year': '2021',
        'amt_cond': '>',
        'amount': '300'
    }
    form = SearchForm(data=data)

    retval = filter_amount(form)

    assert retval.count() == 2
    for i, exp in enumerate(retval):
        assert exp.description == f'Item {i+4}'


def test_search_by_date_limits(db_with_expenses):

    data = {
        'year': '2021',
        'from_date': datetime.date(2021, 1, 6),
        'to_date': datetime.date(2021, 1, 10)
    }
    form = SearchForm(data=data)
    retval = filter_from_to_dates(form)

    assert retval.count() == 5
    for i, exp in enumerate(retval):
        assert exp.description == f'Item {i+6}'


def test_search_by_exact_date(db_with_expenses):

    data = {
        'year': '2021',
        'exact_date': datetime.date(2021, 1, 15)
    }
    form = SearchForm(data=data)
    retval = filter_exact_date(form)

    assert retval.count() == 1
    assert retval.first().description == 'Item 15'


def test_search_by_month(db_with_months_data):

    data = {
        'year': '2021',
        'month': [1, 3]
    }
    form = SearchForm(data=data)
    retval = filter_month(form)

    assert retval.count() == 10
    for i, exp in enumerate(retval):
        if i < 5:
            assert exp.description == f'Item {i+1}'
        else:
            assert exp.description == f'Item {i+6}'


def test_search_no_year(db_with_expenses):

    form = SearchForm()
    retval = filter_year(form)

    assert retval.count() == 15
