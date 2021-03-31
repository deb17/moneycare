from flask import Flask, render_template
from flask_login import current_user
from config import Config
from app.extensions import (
    debug_toolbar,
    db,
    migrate,
    login_manager,
    bootstrap,
    moment
)
from app.blueprints.main import bp as main_bp
from app.blueprints.settings import bp as settings_bp
from app.blueprints.auth import bp as auth_bp
from app.blueprints.expense import bp as expense_bp


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_filters(app)
    register_errorhandlers(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)

    return app


def register_extensions(app):

    debug_toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)


def register_filters(app):

    def format_currency_filter(amount):
        return current_user.currency + ' ' + str(amount)

    app.jinja_env.filters['format_currency'] = format_currency_filter


def register_errorhandlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
