"""Tests d'intégration - Publications"""

from app.models import Post, User


class TestWall:
    def test_wall_public_access(self, client):
        r = client.get("/wall")
        assert r.status_code == 200

    def test_wall_shows_posts(self, client, _post):
        r = client.get("/wall")
        assert r.status_code == 200
        assert b"Message de test" in r.data


class TestCreatePost:
    def test_create_post_authenticated(self, logged_client):
        r = logged_client.post(
            "/post/new",
            data={
                "content": "Nouveau message",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert b"Nouveau message" in r.data

    def test_create_post_unauthenticated(self, client):
        r = client.get("/post/new", follow_redirects=True)
        assert r.status_code == 200
        assert "Connexion" in r.text

    def test_create_post_empty_content(self, logged_client):
        r = logged_client.post(
            "/post/new",
            data={
                "content": "",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert "required" in r.text.lower() or "obligatoire" in r.text.lower()


class TestDeletePost:
    def test_delete_own_post(self, logged_client, db, _post):
        r = logged_client.post(f"/post/{_post.id}/delete", follow_redirects=True)
        assert r.status_code == 200
        assert db.session.get(Post, _post.id) is None

    def test_delete_other_user_post(self, client, app, db, _post):
        other = User(
            last_name="Autre",
            first_name="User",
            email="autre@example.com",
        )
        other.set_password("Pass1234")
        db.session.add(other)
        db.session.commit()

        client.post(
            "/auth/login",
            data={
                "email": "autre@example.com",
                "password": "Pass1234",
            },
        )
        r = client.post(f"/post/{_post.id}/delete")
        assert r.status_code == 403

    def test_delete_as_admin(self, admin_client, db, _post):
        r = admin_client.post(f"/post/{_post.id}/delete", follow_redirects=True)
        assert r.status_code == 200
        assert db.session.get(Post, _post.id) is None
