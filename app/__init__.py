from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.posts import posts_bp
    from app.routes.admin import admin_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)

    with app.app_context():
        db.create_all()
        from app.services.admin import ensure_admin_exists

        ensure_admin_exists(app)

    from app.handlers import register_error_handlers

    register_error_handlers(app)

    @app.context_processor
    def inject_now():
        from datetime import datetime

        return {"now": datetime.utcnow()}

    return app
