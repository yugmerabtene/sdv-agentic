"""Tests unitaires - Modèles"""

from app.models import User, Post


class TestUserModel:
    def test_create_user(self, app, db, _user):
        assert _user.id is not None
        assert _user.last_name == "Dupont"
        assert _user.first_name == "Jean"
        assert _user.email == "jean@example.com"
        assert _user.is_admin is False
        assert _user.is_active_account is True

    def test_password_hashing(self, app, db, _user):
        assert _user.check_password("Password1")
        assert not _user.check_password("WrongPassword")

    def test_password_hash_not_stored_plaintext(self, app, db, _user):
        assert _user.password_hash != "Password1"
        assert _user.password_hash.startswith("scrypt:") or _user.password_hash.startswith(
            "pbkdf2:"
        )


class TestPostModel:
    def test_create_post(self, app, db, _user, _post):
        assert _post.id is not None
        assert _post.content == "Message de test"
        assert _post.author == _user

    def test_post_user_relationship(self, app, db, _user, _post):
        assert _post in _user.posts.all()

    def test_post_cascade_delete(self, app, db, _user, _post):
        user = db.session.get(User, _user.id)
        db.session.delete(user)
        db.session.commit()
        assert Post.query.count() == 0
