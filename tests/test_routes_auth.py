"""Tests d'intégration - Authentification"""

from app.models import User


class TestRegistration:
    def test_register_success(self, client):
        r = client.post(
            "/auth/register",
            data={
                "last_name": "Martin",
                "first_name": "Sophie",
                "email": "sophie@example.com",
                "password": "Pass1234",
                "confirm_password": "Pass1234",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert "Connexion" in r.text

    def test_register_password_mismatch(self, client):
        r = client.post(
            "/auth/register",
            data={
                "last_name": "Martin",
                "first_name": "Sophie",
                "email": "sophie@example.com",
                "password": "Pass1234",
                "confirm_password": "Different1",
            },
            follow_redirects=True,
        )
        assert "ne correspondent pas" in r.text

    def test_register_duplicate_email(self, client, _user):
        r = client.post(
            "/auth/register",
            data={
                "last_name": "Autre",
                "first_name": "User",
                "email": "jean@example.com",
                "password": "Pass1234",
                "confirm_password": "Pass1234",
            },
            follow_redirects=True,
        )
        assert "d\u00e9j\u00e0 utilis\u00e9" in r.text or "utilis" in r.text


class TestLogin:
    def test_login_success(self, client, app, db):
        user = User(last_name="Test", first_name="User", email="test@example.com")
        user.set_password("Password1")
        db.session.add(user)
        db.session.commit()
        r = client.post(
            "/auth/login",
            data={
                "email": "test@example.com",
                "password": "Password1",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert "D\u00e9connexion" in r.text or "Profil" in r.text

    def test_login_invalid_password(self, client, app, db):
        user = User(last_name="Test", first_name="User", email="test@example.com")
        user.set_password("Password1")
        db.session.add(user)
        db.session.commit()
        r = client.post(
            "/auth/login",
            data={
                "email": "test@example.com",
                "password": "WrongPassword1",
            },
            follow_redirects=True,
        )
        assert "invalide" in r.text

    def test_login_invalid_email(self, client):
        r = client.post(
            "/auth/login",
            data={
                "email": "unknown@example.com",
                "password": "Password1",
            },
            follow_redirects=True,
        )
        assert "invalide" in r.text

    def test_login_deactivated_user(self, client, app, db):
        user = User(last_name="Test", first_name="User", email="test@example.com")
        user.set_password("Password1")
        user.is_active_account = False
        db.session.add(user)
        db.session.commit()
        r = client.post(
            "/auth/login",
            data={
                "email": "test@example.com",
                "password": "Password1",
            },
            follow_redirects=True,
        )
        assert "d\u00e9sactiv\u00e9" in r.text or "d\u00e9sactiv" in r.text


class TestLogout:
    def test_logout(self, logged_client):
        r = logged_client.get("/auth/logout", follow_redirects=True)
        assert r.status_code == 200
        assert "Connexion" in r.text
