import pytest

from app.models import Expense, User
from app.models import expense

pytestmark = pytest.mark.nologin


def headers(tok):

    return {'Authorization': f'Bearer {tok}'}


def test_get_expenses(db_with_expenses, token, client):

    resp = client.get('/api/expenses?page=1&page_size=10',
                      headers=headers(token))
    assert resp.status_code == 200

    expenses = resp.get_json()
    assert len(expenses) == 10
    for i, e in enumerate(expenses):
        assert e['description'] == f'Item {15-i}'


def test_get_expense(db_with_expenses, token, client):

    exp = Expense.query.filter_by(description='Item 10').first()
    db_data = {
        'id': exp.id,
        'description': exp.description,
        'amount': exp.amount_str,
        'date': exp.date.isoformat(),
        'payment_mode': exp.payment_mode.mode,
        'estimate': exp.estimate.item if exp.estimate else None,
        'tags': ','.join([tag.tagname for tag in exp.tags]),
        'comments': exp.comments,
        'created_on': exp.created_on.isoformat(),
        'updated_on': exp.updated_on.isoformat()
    }
    resp = client.get(f'/api/expenses/{exp.id}',
                      headers=headers(token))
    assert resp.status_code == 200

    e = resp.get_json()
    assert e == db_data


def test_update_expense(db_with_expenses, token, client):

    # Following code is needed because we are accessing amount
    expense.current_user = User.query.get(1)

    exp = Expense.query.filter_by(description='Item 10').first()
    orig_amount = exp.amount
    orig_comments = exp.comments
    data = {
        'amount': int(orig_amount + 10),
        'comments': 'Amount increased by 10'
    }
    resp = client.patch(f'/api/expenses/{exp.id}',
                        json=data,
                        headers=headers(token))
    assert resp.status_code == 200

    e = resp.get_json()
    assert e['id'] == exp.id
    assert e['amount'] == str(orig_amount + 10)
    assert e['comments'] != orig_comments
    assert e['comments'] == 'Amount increased by 10'


def test_delete_expense(db_with_expenses, token, client):

    exp = Expense.query.filter_by(description='Item 10').first()

    resp = client.delete(f'/api/expenses/{exp.id}', headers=headers(token))
    assert resp.status_code == 204


def test_delete_forbidden(db_with_expenses, token, client):

    exp = Expense.query.filter_by(description='Item user2').first()

    resp = client.delete(f'/api/expenses/{exp.id}', headers=headers(token))
    assert resp.status_code == 403
    assert resp.get_json()['msg'].startswith('Forbidden')


def test_delete_not_found(db_with_expenses, token, client):

    resp = client.delete('/api/expenses/50', headers=headers(token))
    assert resp.status_code == 404
    assert resp.get_json()['msg'] == 'Expense not found.'
