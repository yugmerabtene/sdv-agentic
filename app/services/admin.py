from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User


def ensure_admin_exists(app):
    email = app.config["ADMIN_EMAIL"]
    password = app.config["ADMIN_PASSWORD"]
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return
    user = User(
        last_name="Admin",
        first_name="Admin",
        email=email,
        is_admin=True,
    )
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
