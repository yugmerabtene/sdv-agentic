from datetime import datetime
from app import db


class Post(db.Model):  # type: ignore[name-defined]
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"
