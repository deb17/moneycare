import os
import shutil

import pytest

from app import create_app
from config import TestingConfig, basedir


@pytest.fixture(scope='session')
def app():

    _app = create_app(TestingConfig)

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()

    whoosh_path = os.path.join(basedir, '.indexes-test')
    shutil.rmtree(whoosh_path)
