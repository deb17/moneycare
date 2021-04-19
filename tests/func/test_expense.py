from flask import url_for

from app.models import Expense


def test_new_expense(client):

    params = {
        'description': 'New item X',
        'amount': '123.45',
        'pay_mode': 1,
        'estimate_entry': '',
        'date': '2021-04-01'
    }

    response = client.post(url_for('expense.create'), data=params,
                           follow_redirects=True)

    assert response.status_code == 200
    assert b'New item X' in response.data


def test_list_expenses(client, db_with_expenses):

    page_1 = client.get(url_for('expense.list_expenses'))

    assert page_1.status_code == 200
    for i in range(15, 6, -1):
        assert b'Item ' + str(i).encode() in page_1.data
    assert b'Item 2' not in page_1.data

    page_2 = client.get(url_for('expense.list_expenses', page=2))
    assert page_2.status_code == 200
    assert b'Item 2' in page_2.data


def test_delete_expense(client, db_with_expenses):

    assert Expense.query.count() == 16

    response = client.get(url_for('expense.delete_expense',
                                  id=15,
                                  back='expense.list_expenses'),
                          follow_redirects=True)

    assert response.status_code == 200
    assert Expense.query.count() == 15


def test_delete_expense_forbidden(client, db_with_expenses):

    assert Expense.query.count() == 16
    item = Expense.query.filter_by(description='Item user2').first()

    response = client.get(url_for('expense.delete_expense',
                                  id=item.id,
                                  back='expense.list_expenses'),
                          follow_redirects=True)

    assert response.status_code == 403
    assert Expense.query.count() == 16


def test_edit_expense(client, db_with_expenses):

    exp = Expense.query.filter_by(description='Item 10').first()

    params = {
        'description': 'Item 10 modified',
        'amount': '2000',
        'pay_mode': exp.mode_id,
        'estimate_entry': '',
        'date': str(exp.date),
        'taglist': 'Cash'
    }

    resp = client.post(url_for('expense.edit_expense',
                               id=exp.id,
                               page=1,
                               back='expense.list_expenses'),
                       data=params, follow_redirects=True)

    assert resp.status_code == 200
    assert b'Expense details' in resp.data
    assert b'Item 10 modified' in resp.data
    assert b'2000' in resp.data
    assert b'<span class="badge badge-primary">cash</span>' in resp.data
