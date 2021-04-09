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

    curr_year = datetime.utcnow().year

    items = db.session.query(Budget, Expense) \
        .select_from(Budget) \
        .join(
            Expense,
            db.and_(
                Expense.user_id == Budget.user_id,
                db.func.lower(Budget.item) == db.func.lower(
                    Expense.description)
            )
    ) \
        .filter(
            Budget.user_id == current_user.id,
            db.extract('year', Expense.date) == curr_year
    )
    actual_totals = defaultdict(int)
    for i in items:
        actual_totals[i[0].item] += i[1].amount

    budget_entries = Budget.query \
        .filter(Budget.user_id == current_user.id) \
        .paginate(page, current_app.config['ITEMS_PER_PAGE'], False)

    return render_template('budget/list.html', title='List estimates',
                           totals=actual_totals, entries=budget_entries)


@bp.route('/entry/<int:id>')
@login_required
def get_entry(id):

    page = request.args.get('page', 1, type=int)
    entry = Budget.query.get_or_404(id)

    return render_template('budget/entry.html', title='Estimate entry',
                           entry=entry, page=page)


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
