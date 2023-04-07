from app import db
from app.models import Post, User
from app.post.forms import PostForm
from app.user import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from app.user.forms import ProfileForm


@bp.route("/blog")
def blog():
    """
    Display user posts view
    """
    form = PostForm()
    posts = (
        db.session.query(Post)
        .filter(
            Post.author_id == current_user.id
        )
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template("user/blog.html", posts=posts, form=form)


@bp.route("/profile/<string:username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    user = db.session.query(User).filter(User.username == username).first_or_404()
    form = ProfileForm()
    if form.validate_on_submit():

        user.profile.first_name = form.first_name.data
        user.profile.last_name = form.last_name.data
        user.profile.linkedin = form.linkedin.data
        user.profile.facebook = form.facebook.data
        user.profile.bio = form.bio.data
        db.session.commit()
        flash('Your changes have been saved.', category="success")
        return redirect(url_for('user.profile', username=user.username))
    elif request.method == 'GET':
        form.first_name.data = user.profile.first_name
        form.last_name.data = user.profile.last_name
        form.linkedin.data = user.profile.linkedin
        form.facebook.data = user.profile.facebook
        form.bio.data = user.profile.bio
    return render_template('user/profile.html', user=user, form=form)
