import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret"

import pytest  # noqa: E402
from app import create_app, db as _db  # noqa: E402
from app.models import User, Post  # noqa: E402


@pytest.fixture(scope="function")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test-secret",
        }
    )
    ctx = app.app_context()
    ctx.push()
    _db.create_all()
    yield app
    _db.session.rollback()
    _db.drop_all()
    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    return _db


@pytest.fixture(scope="function")
def _user(app, db):
    u = User(
        last_name="Dupont",
        first_name="Jean",
        email="jean@example.com",
    )
    u.set_password("Password1")
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture(scope="function")
def _admin(app, db):
    a = User(
        last_name="Admin",
        first_name="Admin",
        email="admin@example.com",
        is_admin=True,
    )
    a.set_password("Admin123!")
    db.session.add(a)
    db.session.commit()
    return a


@pytest.fixture(scope="function")
def _post(app, db, _user):
    p = Post(content="Message de test", author=_user)
    db.session.add(p)
    db.session.commit()
    return p


@pytest.fixture(scope="function")
def logged_client(client, _user):
    client.post(
        "/auth/login",
        data={
            "email": "jean@example.com",
            "password": "Password1",
        },
    )
    return client


@pytest.fixture(scope="function")
def admin_client(client, _admin):
    client.post(
        "/auth/login",
        data={
            "email": "admin@example.com",
            "password": "Admin123!",
        },
    )
    return client
