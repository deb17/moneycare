from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class CustomAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()


class CustomModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()


class ExpenseView(CustomModelView):

    column_searchable_list = ('description', 'comments')
    column_filters = ('date',)


class UserView(CustomModelView):

    form_excluded_columns = ('expenses',)
