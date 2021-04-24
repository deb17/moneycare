from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from app.extensions import db
from app.models import Expense, User
from app.models import expense
from .schemas.expense import ExpenseSchema, ExpenseUpdateSchema

bp = Blueprint('api-expense', __name__, url_prefix='/api',
               description='Expense routes')


@bp.route('/expenses')
class ExpenseListResource(MethodView):
    @bp.response(200, ExpenseSchema(exclude=('estimate', 'tags', 'comments',
                                             'created_on', 'updated_on'),
                                    many=True))
    @bp.paginate()
    @bp.doc(security=[{'bearerAuth': []}])
    @jwt_required()
    def get(self, pagination_parameters):
        '''Get all expenses of the user in the current year.'''

        page = pagination_parameters.page
        page_size = pagination_parameters.page_size
        user_id = get_jwt_identity()
        expense.current_user = User.query.get(user_id)
        curr_year = datetime.utcnow().year

        expenses = Expense.query \
            .filter(Expense.user_id == user_id,
                    db.extract('year', Expense.date) == curr_year) \
            .order_by(Expense.date.desc(), Expense.updated_on.desc()) \
            .paginate(page, page_size, False)

        pagination_parameters.item_count = expenses.total
        return expenses.items

    @bp.arguments(ExpenseSchema(exclude=('id',)))
    @bp.response(201, ExpenseSchema)
    @bp.doc(security=[{'bearerAuth': []}])
    @jwt_required()
    def post(self, new_data):
        '''Create new expense.'''

        amount = new_data.pop('amount')
        user_id = get_jwt_identity()
        expense.current_user = User.query.get(user_id)
        exp = Expense(**new_data)
        exp.amount = amount
        exp.user_id = user_id

        db.session.add(exp)
        db.session.commit()

        return exp


@bp.route('/expenses/<int:id>')
class ExpenseResource(MethodView):
    @bp.response(200, ExpenseSchema)
    @bp.doc(security=[{'bearerAuth': []}])
    @jwt_required()
    def get(self, id):

        user_id = get_jwt_identity()
        expense.current_user = User.query.get(user_id)
        exp = Expense.query.get(id)
        if exp:
            if exp.user_id == user_id:
                return exp
            else:
                abort(403, message=(f'Forbidden. Expense {id} not made by '
                                    'current user.'))
        else:
            abort(404, message='Expense not found.')

    @bp.arguments(ExpenseUpdateSchema(exclude=('id',)))
    @bp.response(200, ExpenseSchema)
    @bp.doc(security=[{'bearerAuth': []}])
    @jwt_required()
    def patch(self, update_data, id):

        user_id = get_jwt_identity()
        expense.current_user = User.query.get(user_id)
        query = Expense.query.filter(Expense.id == id)
        exp = query.first()
        if exp:
            if exp.user_id == user_id:
                amount = update_data.pop('amount', None)
                query.update(update_data)
                if amount:
                    exp.amount = amount
                db.session.commit()
                return exp
            else:
                abort(403, message=(f'Forbidden. Expense {id} not made by '
                                    'current user.'))
        else:
            abort(404, message='Expense not found.')

    @bp.response(204)
    @bp.doc(security=[{'bearerAuth': []}])
    @jwt_required()
    def delete(self, id):

        user_id = get_jwt_identity()
        exp = Expense.query.get(id)
        if exp:
            if exp.user_id == user_id:
                db.session.delete(exp)
                db.session.commit()
                return {}
            else:
                abort(403, message=(f'Forbidden. Expense {id} not made by '
                                    'current user.'))
        else:
            abort(404, message='Expense not found.')
