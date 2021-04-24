import shutil
import random
import datetime

import pytest
from flask import url_for
from flask_wtf import FlaskForm

from app import create_app
from app.extensions import db as _db
from app.models import User, Expense, Tag, Budget
from app.models import expense
from config import TestingConfig

FlaskForm.csrf_token = lambda self: ''


@pytest.fixture(scope='session')
def app():

    _app = create_app(TestingConfig)

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()
    shutil.rmtree(TestingConfig.WHOOSH_INDEX_PATH)


@pytest.fixture(scope='function')
def client(app):

    yield app.test_client()


@pytest.fixture(autouse=True, scope='session')
def db(app):

    _db.create_all()

    user1 = User(uname='testuser1', email='test1@test.com')
    user1.set_password('pass123')
    user2 = User(uname='testuser2', email='test2@test.com')
    user2.set_password('pass123')

    _db.session.add_all([user1, user2])
    _db.session.commit()

    return _db


@pytest.fixture(scope='function')
def db_with_expenses(db):

    db.session.query(Expense).delete()

    for i in range(15):
        exp = Expense(
            user_id=1,
            description=('Item ' + str(i + 1)),
            date=datetime.date(2021, 1, i + 1),
            mode_id=random.choice([1, 2])
        )
        exp.amount = random.randrange(100, 1000)
        db.session.add(exp)

    exp_user2 = Expense(
        user_id=2,
        description='Item user2',
        date=datetime.date(2021, 2, 1),
        mode_id=1
    )
    exp_user2.amount = 100
    db.session.add(exp_user2)
    db.session.commit()

    yield

    db.session.query(Expense).delete()
    db.session.commit()

    # remove session else sqlalchemy warning may appear.
    db.session.close()


@pytest.fixture(scope='function')
def db_with_books(db_with_expenses):

    book1 = Expense(
        user_id=1,
        description='Flask cookbook',
        date=datetime.date(2021, 2, 1),
        mode_id=1
    )
    book1.amount = 1200

    book2 = Expense(
        user_id=1,
        description='Rest api',
        comments='Book on Rest api.',
        date=datetime.date(2021, 2, 10),
        mode_id=2
    )
    book2.amount = 1500
    _db.session.add_all([book1, book2])
    _db.session.commit()
    _db.session.close()


@pytest.fixture(scope='function')
def db_with_expense_tags(db):

    db.session.query(Expense).delete()
    db.session.query(Tag).delete()

    tag1 = Tag(tagname='tag1', user_id=1)
    tag2 = Tag(tagname='tag2', user_id=1)
    tag3 = Tag(tagname='tag3', user_id=1)

    for i in range(2):
        exp = Expense(
            user_id=1,
            description=('Item ' + str(i + 1)),
            date=datetime.date(2021, 1, i + 1),
            mode_id=1,
            tags=[tag1]
        )
        exp.amount = 150
        db.session.add(exp)

    exp = Expense(
        user_id=1,
        description='Item 3',
        date=datetime.date(2021, 1, 3),
        mode_id=1,
        tags=[tag1, tag2, tag3]
    )
    exp.amount = 200
    db.session.add(exp)

    for i in range(4, 6):
        exp = Expense(
            user_id=1,
            description=('Item ' + str(i)),
            date=datetime.date(2021, 1, i),
            mode_id=1,
            tags=[tag2]
        )
        exp.amount = 250
        db.session.add(exp)

    db.session.commit()

    yield

    db.session.query(Expense).delete()
    db.session.query(Tag).delete()
    db.session.commit()
    db.session.close()


@pytest.fixture(scope='function')
def db_with_expense_amounts(db):

    expense.current_user = User.query.get(1)
    db.session.query(Expense).delete()
    amts = [150, 200, 300, 350, 400]

    for i in range(5):
        exp = Expense(
            user_id=1,
            description=('Item ' + str(i + 1)),
            date=datetime.date(2021, 1, i + 1),
            mode_id=1
        )
        exp.amount = amts[i]
        db.session.add(exp)

    db.session.commit()

    yield

    db.session.query(Expense).delete()
    db.session.commit()
    db.session.close()


@pytest.fixture(scope='function')
def db_with_months_data(db):

    db.session.query(Expense).delete()

    k = 0
    for i in range(3):
        for j in range(5):
            k += 1
            exp = Expense(
                user_id=1,
                description=('Item ' + str(k)),
                date=datetime.date(2021, i + 1, j + 1),
                mode_id=1
            )
            exp.amount = 100
            db.session.add(exp)

    db.session.commit()

    yield

    db.session.query(Expense).delete()
    db.session.commit()
    db.session.close()


@pytest.fixture(scope='function')
def db_with_related_expenses(db):
    '''An expense can be related to a budget entry either by foreign
    key or by same description.
    '''

    db.session.query(Expense).delete()
    db.session.query(Budget).delete()

    budget_entry = Budget(user_id=1, item='Budget item 1', estimate=5000)
    related_expenses = []
    dates = [datetime.date(2020, 10, 20), datetime.date(2021, 2, 5)]
    amount = 1000
    for i in range(2):
        exp = Expense(
            user_id=1,
            description='Related expense',
            date=dates[i],
            mode_id=1
        )
        amount += 1000
        exp.amount = amount
        related_expenses.append(exp)
    budget_entry.expenses = related_expenses

    db.session.add(budget_entry)

    related_expense = Expense(
        user_id=1,
        description='Budget item 1',
        date=datetime.date(2021, 3, 2),
        mode_id=1
    )
    related_expense.amount = 500
    db.session.add(related_expense)

    # other expenses
    for i in range(5):
        exp = Expense(
            user_id=1,
            description=('Item ' + str(i + 1)),
            date=datetime.date(2021, 2, i + 1),
            mode_id=1
        )
        exp.amount = 100
        db.session.add(exp)

    db.session.commit()

    yield

    db.session.query(Expense).delete()
    db.session.query(Budget).delete()
    db.session.commit()
    db.session.close()


@pytest.fixture(scope='function')
def db_with_budget_expenses(db):

    db.session.query(Expense).delete()
    db.session.query(Budget).delete()

    desc = ['Item 1'] * 3 + ['Item 2'] * 2
    amount = 1000
    for i in range(5):
        exp = Expense(
            user_id=1,
            description=desc[i],
            date=datetime.date(2021, 2, i + 1),
            mode_id=1
        )
        exp.amount = amount
        amount += 1000
        db.session.add(exp)

    db.session.commit()

    yield

    db.session.query(Expense).delete()
    db.session.query(Budget).delete()
    db.session.commit()
    db.session.close()


@pytest.fixture(autouse=True, scope='function')
def authenticate(db, client, request):

    if 'nologin' in request.keywords:
        yield
    else:
        params = {
            'identity': 'testuser1',
            'password': 'pass123'
        }

        client.post(url_for('auth.login'), data=params,
                    follow_redirects=True)

        yield

        client.get(url_for('auth.logout'), follow_redirects=True)


@pytest.fixture(scope='module')
def token(app, db):

    # not using client fixture because the token fixture is module
    # scoped while the client fixture is function scoped
    client = app.test_client()

    login_data = {
        'username': 'testuser1',
        'password': 'pass123'
    }

    resp = client.post('/api/login', json=login_data)
    token = resp.get_json()['access_token']
    return token
