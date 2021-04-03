from datetime import datetime

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.blueprints.main.forms import DashboardYearForm
from app.blueprints.main.utils import get_context
from app.models import Expense

bp = Blueprint('main', __name__)


@bp.route('/')
def index():

    return render_template('main/index.html')


@bp.route('/home')
@login_required
def home():

    return 'test'


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form = DashboardYearForm()

    years = db.session.query(db.extract('year', Expense.date).label('year')) \
        .filter(Expense.user_id == current_user.id) \
        .distinct() \
        .order_by(db.text('year asc'))
    form.year.choices = [('', 'Year')] + [(y[0], str(y[0])) for y in years]

    ctx = {}
    if form.validate_on_submit():
        year = int(form.year.data)
        ctx = get_context(year)
    elif request.method == 'GET':
        current_year = datetime.utcnow().year
        ctx = get_context(current_year)

    return render_template('main/dashboard.html', form=form, ctx=ctx,
                           title='Dashboard')
