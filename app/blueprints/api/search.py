from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.models import User
from app.models import expense
from .schemas.expense import ExpenseSchema
from .schemas.search import SearchSchema
from app.blueprints.search.forms import SearchForm
from app.blueprints.search.utils import search_main
from app.blueprints.search import utils


bp = Blueprint('api-search', __name__, url_prefix='/api',
               description='Search route')


@bp.route('/search')
class SearchResource(MethodView):
    @bp.arguments(SearchSchema(exclude=('id', 'date', 'description',
                                        'comments')))
    @bp.response(200, ExpenseSchema(many=True))
    @bp.paginate()
    @bp.doc(security=[{'bearerAuth': []}])
    @jwt_required()
    def post(self, search_data, pagination_parameters):
        '''Get all expenses of the user in the current year.'''

        page = pagination_parameters.page
        page_size = pagination_parameters.page_size
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        expense.current_user = user
        utils.current_user = user

        form = SearchForm(data=search_data)
        result, _ = search_main(form, page, page_size)
        pagination_parameters.item_count = result.total
        if result.total == 0:
            abort(404, message='No search results')

        return result.items
