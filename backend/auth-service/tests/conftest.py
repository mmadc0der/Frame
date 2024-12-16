import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app('app.config.TestingConfig')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()
