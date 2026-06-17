from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from app import db
from app.forms.profile import ProfileForm, ChangePasswordForm, DeleteAccountForm

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/")
@login_required
def view():
    return render_template("profile/view.html")


@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.last_name = form.last_name.data
        current_user.first_name = form.first_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Profil mis à jour.", "success")
        return redirect(url_for("profile.view"))
    return render_template("profile/edit.html", form=form)


@profile_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Mot de passe actuel incorrect.", "danger")
            return render_template("profile/change_password.html", form=form)
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Mot de passe modifié.", "success")
        return redirect(url_for("profile.view"))
    return render_template("profile/change_password.html", form=form)


@profile_bp.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.password.data):
            flash("Mot de passe incorrect.", "danger")
            return render_template("profile/delete.html", form=form)
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        flash("Votre compte a été supprimé.", "info")
        return redirect(url_for("auth.register"))
    return render_template("profile/delete.html", form=form)
