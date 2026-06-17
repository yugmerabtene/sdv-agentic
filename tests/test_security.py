"""Tests de sécurité"""


class TestXSSProtection:
    def test_post_content_escaped(self, logged_client):
        r = logged_client.post(
            "/post/new",
            data={
                "content": "<script>alert('xss')</script>",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert b"<script>" not in r.data
        assert b"&lt;script&gt;" in r.data


class TestAccessControl:
    def test_unauthenticated_cannot_post(self, client):
        r = client.get("/post/new", follow_redirects=True)
        assert "Connexion" in r.text

    def test_regular_user_cannot_access_admin(self, logged_client):
        r = logged_client.get("/admin/users")
        assert r.status_code == 403


class TestPasswordStrength:
    def test_weak_password_rejected(self, client):
        r = client.post(
            "/auth/register",
            data={
                "last_name": "Test",
                "first_name": "User",
                "email": "weak@example.com",
                "password": "weak",
                "confirm_password": "weak",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert "8 caract" in r.text or "courte" in r.text or "required" in r.text.lower()
