from flask_admin import Admin

from app.extensions import db
from app.models import (
    User,
    Expense,
    Social,
    Tag,
    PaymentMode,
    Budget
)
from app.blueprints.admin.controllers import (
    CustomAdminIndexView,
    CustomModelView,
    ExpenseView,
    UserView
)

admin = Admin(
    index_view=CustomAdminIndexView(),
    base_template='admin/admin-master.html',
    template_mode='bootstrap3'
)


def admin_create_module(app):

    admin.init_app(app)

    admin.add_view(UserView(User, db.session))
    admin.add_view(ExpenseView(Expense, db.session, endpoint='expenses'))

    models = [Social, Tag, PaymentMode, Budget]

    for model in models:
        admin.add_view(CustomModelView(model, db.session))
