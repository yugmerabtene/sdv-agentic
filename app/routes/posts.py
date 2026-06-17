from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post
from app.forms.post import PostForm

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/")
@posts_bp.route("/wall")
def wall():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template("posts/wall.html", posts=posts)


@posts_bp.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Votre publication a été créée.", "success")
        return redirect(url_for("posts.wall"))
    return render_template("posts/create.html", form=form)


@posts_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Publication supprimée.", "success")
    return redirect(url_for("posts.wall"))
