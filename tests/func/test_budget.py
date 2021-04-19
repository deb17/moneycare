from flask import url_for


def test_new_budget_entry(client, db_with_budget_expenses):

    params = {
        'item': 'Item 1',
        'estimate': 4000,
        'active': True
    }

    response = client.post(url_for('budget.new_entry'), data=params,
                           follow_redirects=True)

    assert response.status_code == 200
    assert b'MoneyCare - Budget' in response.data

    response = client.get(url_for('budget.list_entries'))

    assert response.status_code == 200
    assert b'4000' in response.data  # 4000 is the estimate value
    assert b'6000' in response.data  # 6000 is the total of 3 related txns
    assert b'Over' in response.data


def test_related_expenses(client, db_with_related_expenses):

    response = client.get(url_for('budget.related_expenses', page=1,
                                  budget_id=1, budget_page=1))

    assert response.status_code == 200
    assert b'Total number of transactions is 2' in response.data
    assert b'Budget item 1' in response.data
    assert b'Related expense' in response.data
    assert b'2000' not in response.data  # One expense is not in current year
    assert b'3000' in response.data
