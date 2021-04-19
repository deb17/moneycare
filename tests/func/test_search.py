from flask import url_for


def test_search_with_multiple_conditions(client, db_with_books):

    params = {
        'year': '2021',
        'month': [2],
        'from_date': '2021-02-05',
        'amt_cond': '==',
        'amt_min': '1000',
        'text': 'book',
        'simple_search': True
    }

    response = client.post(url_for('search.index'), data=params,
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Rest api' in response.data
    assert b'Flask cookbook' not in response.data
