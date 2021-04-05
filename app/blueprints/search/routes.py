from flask import Blueprint
from flask_login import login_required

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route('/')
@login_required
def index():

    return 'test'
