from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from app.blueprints.budget.forms import BudgetForm
from app.models import Budget
from app.extensions import db

bp = Blueprint('budget', __name__, url_prefix='/budget')


@bp.route('/')
def home():

    return render_template('budget/index.html', title='Budget')


@bp.route('/new')
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
def list_entries():

    return 'test'
