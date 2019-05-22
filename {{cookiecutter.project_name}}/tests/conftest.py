import json
import pytest

from {{cookiecutter.app_name}}.models import Example
from {{cookiecutter.app_name}}.app import create_app
from {{cookiecutter.app_name}}.extensions import db as _db


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    entry = Example(
        name='example-test',
    )

    db.session.add(entry)
    db.session.commit()

    return entry
