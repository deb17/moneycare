import pytest

pytestmark = pytest.mark.nologin


def headers(tok):

    return {'Authorization': f'Bearer {tok}'}


def test_search_text(db_with_books, token, client):

    data = {
        'text': 'book',
        'simple_search': True
    }

    resp = client.post('/api/search', json=data, headers=headers(token))
    assert resp.status_code == 200

    retval = resp.get_json()
    assert len(retval) == 2
    assert retval[0]['description'] == 'Rest api'


def test_search_text_with_whoosh(db_with_books, token, client):

    data = {
        'text': 'book'
    }

    resp = client.post('/api/search', json=data, headers=headers(token))
    assert resp.status_code == 200

    retval = resp.get_json()
    assert len(retval) == 1
    assert retval[0]['description'] == 'Rest api'


def test_search_invalid_year(db_with_books, token, client):

    data = {
        'year': '2200',
        'text': 'book',
        'simple_search': True
    }

    resp = client.post('/api/search', json=data, headers=headers(token))
    assert resp.status_code == 422

    retval = resp.get_json()
    assert retval['errors']['json']['year'] == ['Year is invalid']


def test_search_not_found(db_with_expenses, token, client):

    data = {
        'year': '2021',
        'text': 'xyz'
    }

    resp = client.post('/api/search', json=data, headers=headers(token))
    assert resp.status_code == 404

    retval = resp.get_json()
    assert retval['msg'] == 'No search results'


def test_search_amount(db_with_expense_amounts, token, client):

    data = {
        'year': '2021',
        'amount': 200
    }

    resp = client.post('/api/search', json=data, headers=headers(token))
    assert resp.status_code == 200

    retval = resp.get_json()
    assert len(retval) == 1
    assert retval[0]['description'] == 'Item 2'
    assert retval[0]['amount'] == '200.00'


def test_search_amount_field_mismatch(db_with_expense_amounts, token, client):

    data = {
        'year': '2021',
        'amount': 200,
        'amt_min': 100
    }

    resp = client.post('/api/search', json=data, headers=headers(token))
    assert resp.status_code == 422

    retval = resp.get_json()
    assert (retval['errors']['json']['_schema'] ==
            ['Both amount and amt_min cannot be specified.'])


def test_search_multiple_conditions(db_with_expense_amounts, token, client):

    data = {
        'year': '2021',
        'text': 'item',
        'simple_search': True,
        'amt_min': 300,
        'from_date': '2021-01-04'
    }

    resp = client.post('/api/search', json=data, headers=headers(token))
    assert resp.status_code == 200

    retval = resp.get_json()
    assert len(retval) == 2
    assert retval[0]['description'] == 'Item 5'
    assert retval[0]['amount'] == '400.00'
    assert retval[1]['description'] == 'Item 4'
    assert retval[1]['amount'] == '350.00'
