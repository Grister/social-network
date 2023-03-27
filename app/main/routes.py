# from app import app
from app.main import bp
from flask import render_template


# register routes
@bp.route("/")
@bp.route("/index")
def index():
    # sample template context to render
    context = {
        "user": {"username": "Zakhar"},
        "title": "Hillel"
    }
    return render_template("index.html", **context)


@bp.route("/about")
def about():
    return render_template("about.html")
