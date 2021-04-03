import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') or 'topsecretkey'
    DEFAULT_COUNTRY_CODE = 'US'
    DEFAULT_CURRENCY = 'USD'
    DEFAULT_LOCALE = 'en-US'
    ITEMS_PER_PAGE = 10
    GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
    OAUTHLIB_RELAX_TOKEN_SCOPE = True
    TWITTER_OAUTH_CLIENT_KEY = os.getenv('TWITTER_OAUTH_CLIENT_KEY')
    TWITTER_OAUTH_CLIENT_SECRET = os.getenv('TWITTER_OAUTH_CLIENT_SECRET')
