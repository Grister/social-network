from app import db
from app.main import bp
from flask import render_template

from app.models import Post


@bp.route("/")
@bp.route("/index")
def index():
    posts = db.session.query(Post).order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)


@bp.route('/about')
def about():
    return render_template("about.html")
