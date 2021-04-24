import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'topsecretkey'
    DEFAULT_COUNTRY_CODE = 'US'
    DEFAULT_CURRENCY = 'USD'
    DEFAULT_LOCALE = 'en-US'
    ITEMS_PER_PAGE = 10
    SEARCH_ITEMS_PER_PAGE = 5

    GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
    OAUTHLIB_RELAX_TOKEN_SCOPE = True
    TWITTER_OAUTH_CLIENT_KEY = os.getenv('TWITTER_OAUTH_CLIENT_KEY')
    TWITTER_OAUTH_CLIENT_SECRET = os.getenv('TWITTER_OAUTH_CLIENT_SECRET')

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    FLASK_ADMIN_SWATCH = 'cerulean'

    API_TITLE = 'MoneyCare API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/api/docs'
    OPENAPI_SWAGGER_UI_PATH = '/'
    OPENAPI_SWAGGER_UI_URL = (
        'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.47.1/'
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    SENTRY_URL = os.getenv('SENTRY_URL')


class TestingConfig(Config):

    TESTING = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WHOOSH_INDEX_PATH = os.path.join(basedir, 'tests', '.indexes-test')
