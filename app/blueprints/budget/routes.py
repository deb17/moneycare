from datetime import datetime
from collections import defaultdict

from flask import (Blueprint, render_template, redirect, url_for, flash,
                   current_app, request, abort)
from flask_login import current_user, login_required

from app.blueprints.budget.forms import BudgetForm
from app.models import Budget, Expense
from app.extensions import db

bp = Blueprint('budget', __name__, url_prefix='/budget')


@bp.route('/')
@login_required
def home():

    return render_template('budget/index.html', title='Budget')


@bp.route('/entry/new', methods=['GET', 'POST'])
@login_required
def new_entry():

    form = BudgetForm()

    if form.validate_on_submit():
        budg = Budget(user_id=current_user.id)
        form.populate_obj(budg)
        db.session.add(budg)
        db.session.commit()
        flash('A new estimate entry was created.', 'success')
        return redirect(url_for('budget.home'))

    return render_template('budget/new.html', title='New entry', form=form)


@bp.route('/list')
@bp.route('/list/<int:page>')
@login_required
def list_entries(page=1):
    '''Aggregate expenses for each budget entry by either -
    1. Matching descriptions case insensitively (the user may have
       forgotten to select an estimate while creating the expense).
    2. Finding expenses by foreign key
    '''

    curr_year = datetime.utcnow().year

    E = Expense

    expense_subq = db.session.query(E.description, E.amount_str) \
        .filter(
            E.user_id == current_user.id,
            db.extract('year', E.date) == curr_year,
            E.budget_id.is_(None)
    ).subquery()

    budget_subq = db.session.query(Budget.item).filter(
        Budget.user_id == current_user.id
    ).subquery()

    q = db.session.query(budget_subq, expense_subq) \
        .select_from(budget_subq) \
        .join(
            expense_subq,
            (db.func.lower(budget_subq.c.item) ==
                db.func.lower(expense_subq.c.description))
    )
    actual_totals = defaultdict(int)
    for item, _, amount_str in q:
        actual_totals[item] += E.amount_num(amount_str)

    budget_entries = Budget.query \
        .filter(Budget.user_id == current_user.id) \
        .paginate(page, current_app.config['ITEMS_PER_PAGE'], False)

    for entry in budget_entries.items:
        for exp in entry.expenses:
            actual_totals[entry.item] += exp.amount

    return render_template('budget/list.html', title='List estimates',
                           totals=actual_totals, entries=budget_entries)


@bp.route('/entry/<int:id>')
@login_required
def get_entry(id):

    page = request.args.get('page', 1, type=int)
    entry = Budget.query.get_or_404(id)

    return render_template('budget/entry.html', title='Estimate entry',
                           entry=entry, page=page)


@bp.route('/entry/related-expenses/<int:page>')
@login_required
def related_expenses(page):

    budget_id = request.args.get('budget_id', type=int)
    budget_page = request.args.get('budget_page', type=int)

    curr_year = datetime.utcnow().year

    E = Expense

    expense_subq = db.session.query(
        E.id,
        E.date,
        E.description,
        E.budget_id
    ) \
        .filter(
            E.user_id == current_user.id,
            db.extract('year', E.date) == curr_year
    ).subquery()

    budget_subq = db.session.query(Budget).filter(
        Budget.user_id == current_user.id
    ).subquery()

    expenses = db.session.query(expense_subq) \
        .select_from(budget_subq) \
        .join(
            expense_subq,
            db.or_((db.func.lower(budget_subq.c.item) ==
                    db.func.lower(expense_subq.c.description)),
                   budget_subq.c.id == expense_subq.c.budget_id)
    ) \
        .order_by(expense_subq.c.date.desc()) \
        .paginate(page, current_app.config['ITEMS_PER_PAGE'], False)

    page_ids = [item.id for item in expenses.items]
    expenses.items = E.query.filter(E.id.in_(page_ids)) \
        .order_by(E.date.desc()).all()

    return render_template('budget/expenses.html', title='Related expenses',
                           budget_id=budget_id, budget_page=budget_page,
                           expenses=expenses)


@bp.route('/entry/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):

    page = request.args.get('page', 1, type=int)
    entry = Budget.query.get_or_404(id)
    if entry.user_id != current_user.id:
        abort(403)
    form = BudgetForm(obj=entry)

    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
        flash('The estimate was updated.', 'success')
        return redirect(url_for('budget.get_entry', id=id, page=page))

    return render_template('budget/edit.html', title='Edit estimate',
                           form=form, page=page, id=entry.id)


@bp.route('/entry/delete/<int:id>')
@login_required
def delete_entry(id):

    entry = Budget.query.get_or_404(id)
    if entry.user_id != current_user.id:
        abort(403)

    db.session.delete(entry)
    db.session.commit()
    flash('The estimate was deleted.', 'success')

    return redirect(url_for('budget.home'))
