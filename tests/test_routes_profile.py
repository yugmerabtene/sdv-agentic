"""Tests d'intégration - Profil"""

from app.models import User


class TestProfileView:
    def test_view_profile_authenticated(self, logged_client):
        r = logged_client.get("/profile/")
        assert r.status_code == 200
        assert b"Jean" in r.data

    def test_view_profile_unauthenticated(self, client):
        r = client.get("/profile/", follow_redirects=True)
        assert r.status_code == 200
        assert "Connexion" in r.text


class TestProfileEdit:
    def test_edit_profile(self, logged_client):
        r = logged_client.post(
            "/profile/edit",
            data={
                "last_name": "Durand",
                "first_name": "Pierre",
                "email": "jean@example.com",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert b"Durand" in r.data

    def test_edit_profile_duplicate_email(self, logged_client, app, db):
        other = User(
            last_name="Autre",
            first_name="User",
            email="autre@example.com",
        )
        other.set_password("Pass1234")
        db.session.add(other)
        db.session.commit()
        r = logged_client.post(
            "/profile/edit",
            data={
                "last_name": "Jean",
                "first_name": "Dupont",
                "email": "autre@example.com",
            },
            follow_redirects=True,
        )
        assert "d\u00e9j\u00e0 utilis\u00e9" in r.text or "utilis" in r.text


class TestChangePassword:
    def test_change_password_success(self, logged_client):
        r = logged_client.post(
            "/profile/change-password",
            data={
                "current_password": "Password1",
                "new_password": "NewPass123",
                "confirm_password": "NewPass123",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert "modifi\u00e9" in r.text

    def test_change_password_wrong_current(self, logged_client):
        r = logged_client.post(
            "/profile/change-password",
            data={
                "current_password": "WrongPass1",
                "new_password": "NewPass123",
                "confirm_password": "NewPass123",
            },
            follow_redirects=True,
        )
        assert "incorrect" in r.text


class TestDeleteAccount:
    def test_delete_account_success(self, logged_client):
        r = logged_client.post(
            "/profile/delete",
            data={
                "password": "Password1",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert "Inscription" in r.text

    def test_delete_account_wrong_password(self, logged_client):
        r = logged_client.post(
            "/profile/delete",
            data={
                "password": "WrongPass1",
            },
            follow_redirects=True,
        )
        assert "incorrect" in r.text
