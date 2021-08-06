from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
moment = Moment()
mail = Mail()

api = Api()
api.DEFAULT_ERROR_RESPONSE_NAME = None

jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
