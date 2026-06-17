"""Tests d'intégration - Administration"""

from app.models import User


class TestAdminAccess:
    def test_admin_users_list(self, admin_client):
        r = admin_client.get("/admin/users")
        assert r.status_code == 200
        assert b"Admin" in r.data or b"admin" in r.data

    def test_non_admin_cannot_access(self, logged_client):
        r = logged_client.get("/admin/users")
        assert r.status_code == 403

    def test_unauthenticated_cannot_access(self, client):
        r = client.get("/admin/users", follow_redirects=True)
        assert r.status_code == 200
        assert "Connexion" in r.text


class TestAdminDeleteUser:
    def test_admin_delete_user(self, admin_client, app, db, _user):
        assert db.session.get(User, _user.id) is not None
        r = admin_client.post(f"/admin/users/{_user.id}/delete", follow_redirects=True)
        assert r.status_code == 200
        assert db.session.get(User, _user.id) is None

    def test_admin_cannot_delete_admin(self, admin_client, app, db, _admin):
        r = admin_client.post(f"/admin/users/{_admin.id}/delete", follow_redirects=True)
        assert r.status_code == 200
        assert db.session.get(User, _admin.id) is not None


class TestAdminToggleActive:
    def test_admin_deactivate_user(self, admin_client, app, db, _user):
        r = admin_client.post(f"/admin/users/{_user.id}/toggle-active", follow_redirects=True)
        assert r.status_code == 200
        u = db.session.get(User, _user.id)
        assert u.is_active_account is False

    def test_admin_reactivate_user(self, admin_client, app, db, _user):
        _user.is_active_account = False
        db.session.commit()
        r = admin_client.post(f"/admin/users/{_user.id}/toggle-active", follow_redirects=True)
        assert r.status_code == 200
        u = db.session.get(User, _user.id)
        assert u.is_active_account is True
