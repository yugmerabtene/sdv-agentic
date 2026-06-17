from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms.auth import RegistrationForm, LoginForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("posts.wall"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            last_name=form.last_name.data,
            first_name=form.first_name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Votre compte a été créé avec succès.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("posts.wall"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Email ou mot de passe invalide.", "danger")
            return render_template("auth/login.html", form=form)
        if not user.is_active_account:
            flash("Ce compte a été désactivé.", "danger")
            return render_template("auth/login.html", form=form)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        flash("Connexion réussie.", "success")
        return redirect(next_page) if next_page else redirect(url_for("posts.wall"))
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("auth.login"))
