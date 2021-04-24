from flask import Flask, render_template, jsonify
from flask_login import current_user
from config import Config
from app.extensions import (
    debug_toolbar,
    db,
    migrate,
    login_manager,
    bootstrap,
    moment,
    mail,
    api,
    jwt
)
from app.blueprints.main import bp as main_bp
from app.blueprints.settings import bp as settings_bp
from app.blueprints.auth import (bp as auth_bp, google_blueprint,
                                 twitter_blueprint)
from app.blueprints.expense import bp as expense_bp
from app.blueprints.search import bp as search_bp
from app.blueprints.budget import bp as budget_bp
from app.blueprints.admin import admin_create_module
from app.blueprints.api import (
    api_user_bp,
    api_expense_bp,
    api_search_bp
)


def create_app(config=Config):

    app = Flask(__name__)
    app.config.from_object(config)

    admin_create_module(app)
    register_extensions(app)
    register_filters(app)
    register_errorhandlers(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(google_blueprint)
    app.register_blueprint(twitter_blueprint)
    app.register_blueprint(expense_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(budget_bp)

    setup_for_api(api)
    api.register_blueprint(api_user_bp)
    api.register_blueprint(api_expense_bp)
    api.register_blueprint(api_search_bp)

    return app


def register_extensions(app):

    debug_toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    api.init_app(app)
    jwt.init_app(app)


def setup_for_api(api):

    import warnings
    warnings.filterwarnings(
        "ignore",
        message="Multiple schemas resolved to the name "
    )

    api.spec.components.security_scheme(
        'bearerAuth',
        {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'}
    )


def register_filters(app):

    def format_currency_filter(amount):
        return current_user.currency + ' ' + str(amount)

    app.jinja_env.filters['format_currency'] = format_currency_filter


def register_errorhandlers(app):

    @app.errorhandler(404)
    def page_not_found(error):

        if hasattr(error, 'data'):
            response = jsonify(msg=error.data['message'])
            response.status_code = 404
            return response
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(error):

        if hasattr(error, 'data'):
            response = jsonify(msg=error.data['message'])
            response.status_code = 403
            return response
        return render_template('errors/403.html'), 403
