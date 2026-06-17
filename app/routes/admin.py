from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    users_list = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users_list)


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("Impossible de supprimer un administrateur.", "danger")
        return redirect(url_for("admin.users"))
    db.session.delete(user)
    db.session.commit()
    flash(f"L'utilisateur {user.email} a été supprimé.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/toggle-active", methods=["POST"])
@login_required
@admin_required
def toggle_active(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("Impossible de désactiver un administrateur.", "danger")
        return redirect(url_for("admin.users"))
    user.is_active_account = not user.is_active_account
    db.session.commit()
    status = "activé" if user.is_active_account else "désactivé"
    flash(f"Le compte de {user.email} a été {status}.", "success")
    return redirect(url_for("admin.users"))
