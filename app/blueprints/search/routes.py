from datetime import datetime

from flask import (Blueprint, render_template, flash,
                   redirect, url_for, request, current_app)
from flask_login import login_required, current_user
import flask_whooshalchemy

from app.blueprints.search.forms import SearchForm
from app.blueprints.search.utils import search_main, to_session, from_session
from app.models import Expense, PaymentMode, Tag

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.before_app_first_request
def bootstrap():

    flask_whooshalchemy.search_index(current_app, Expense)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

    curr_year = datetime.utcnow().year
    tags = Tag.query.filter_by(user_id=current_user.id).all()
    tag_choices = [(t.id, t.tagname) for t in tags]

    modes = PaymentMode.query.filter_by(user_id=current_user.id).all()
    mode_choices = [(m.id, m.mode) for m in modes]

    form = SearchForm(year=curr_year)
    form.tags.choices = tag_choices
    form.payment_modes.choices = mode_choices

    if form.validate_on_submit():
        to_session(form)
        return redirect(url_for('search.search_results'))

    if form.errors:
        flash('Form has errors.', 'danger')

    return render_template('search/index.html', form=form, title='Search')


@bp.route('/results')
@login_required
def search_results():

    page = request.args.get('page', 1, type=int)

    form_data = from_session()
    form = SearchForm(data=form_data)

    expenses, total = search_main(form, page)
    if form.text.data and not form.simple_search.data:
        whoosh = True
    else:
        whoosh = False

    return render_template('search/search_results.html',
                           title='Search results',
                           expenses=expenses,
                           total=total, whoosh=whoosh)
