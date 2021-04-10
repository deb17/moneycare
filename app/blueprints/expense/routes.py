from datetime import datetime

from flask import (Blueprint, render_template, redirect, url_for, flash,
                   current_app, request, abort)
from flask_login import login_required, current_user

from app.models import Expense, PaymentMode, Budget
from app.extensions import db
from app.blueprints.expense.forms import ExpenseForm

bp = Blueprint('expense', __name__, url_prefix='/expense')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    form = ExpenseForm()
    modes = PaymentMode.query.filter_by(user_id=current_user.id)
    form.pay_mode.choices = [('', 'Choose one')] + [
        (m.id, m.mode) for m in modes
    ]
    estimates = Budget.query.filter(
        Budget.user_id == current_user.id,
        Budget.active.is_(True)
    )
    form.estimate_entry.choices = [('', 'Choose one')] + [
        (e.id, e.item) for e in estimates
    ]

    if form.validate_on_submit():
        e = Expense()
        e.user_id = current_user.id
        e.description = form.description.data
        e.date = form.date.data
        e.amount = form.amount.data
        e.mode_id = int(form.pay_mode.data)
        e.budget_id = (int(form.estimate_entry.data) if
                       form.estimate_entry.data else None)
        e.comments = form.comments.data
        e.set_tags(form.taglist.data)
        db.session.add(e)
        db.session.commit()
        flash('New expense created.', 'success')
        return redirect(url_for('expense.list_expenses'))

    return render_template('expense/new.html', title='New expense',
                           form=form, heading='Create new expense')


@bp.route('/list')
@bp.route('/list/<int:page>')
@login_required
def list_expenses(page=1):

    year = datetime.utcnow().year
    expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        db.extract('year', Expense.date) == year) \
        .order_by(Expense.date.desc(), Expense.updated_on.desc()) \
        .paginate(page, current_app.config['ITEMS_PER_PAGE'])

    return render_template('expense/list.html', title='List expenses',
                           expenses=expenses, year=year)


@bp.route('/<int:id>')
@login_required
def get_expense(id):

    page = request.args.get('page', 1)
    back = request.args.get('back')
    expense = Expense.query.get_or_404(id)

    return render_template('expense/expense.html', exp=expense,
                           title='Expense', page=page, back=back)


@bp.route('/delete/<int:id>')
@login_required
def delete_expense(id):

    exp = Expense.query.get(id)
    back = request.args.get('back')
    if exp.user_id != current_user.id:
        abort(403)
    db.session.delete(exp)
    db.session.commit()
    flash('The expense was deleted.', 'success')

    return redirect(url_for(back))


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):

    page = request.args.get('page', 1)
    back = request.args.get('back')
    exp = Expense.query.get(id)

    if current_user.id != exp.user_id:
        abort(403)

    tags = ','.join([t.tagname for t in exp.tags])

    form = ExpenseForm(obj=exp,
                       pay_mode=exp.mode_id,
                       estimate_entry=exp.budget_id,
                       taglist=tags)
    modes = PaymentMode.query.filter_by(user_id=current_user.id)
    form.pay_mode.choices = [(m.id, m.mode) for m in modes]
    estimates = Budget.query.filter(
        Budget.user_id == current_user.id,
        db.or_(Budget.active.is_(True), Budget.id == exp.budget_id)
    )
    if exp.budget_id:
        select_prompt = []
    else:
        select_prompt = [('', 'Choose one')]
    form.estimate_entry.choices = (select_prompt +
                                   [(e.id, e.item) for e in estimates])

    if form.validate_on_submit():
        form.populate_obj(exp)
        exp.mode_id = int(form.pay_mode.data)
        exp.budget_id = (int(form.estimate_entry.data) if
                         form.estimate_entry.data else None)
        exp.tags = []
        exp.set_tags(form.taglist.data)
        db.session.commit()
        flash('The expense was updated.', 'success')
        return redirect(url_for('expense.get_expense', id=id, page=page,
                                back=back))

    return render_template('expense/edit.html', title='Edit expense',
                           form=form, heading='Edit expense', id=id,
                           page=page, back=back)
