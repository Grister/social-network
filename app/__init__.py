from datetime import datetime

from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()


def create_app():
    """
    Application factory method to create application
    :return: Flask application configured object
    """

    # create instance of Flask object
    app = Flask(__name__)

    # update application config from Config class in config.py
    app.config.from_object(Config)

    # install extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    jwt.init_app(app)

    # register blueprints here
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .faker import bp as fake_bp
    app.register_blueprint(fake_bp)

    from .user import bp as user_bp
    app.register_blueprint(user_bp)

    from .post import bp as post_bp
    app.register_blueprint(post_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp)

    from . import models  # noqa

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(user_id)

    @app.context_processor
    def context_processor():
        return dict(
            current_user=current_user
        )
    return app


# create instance of application
app = create_app()


@app.before_request
def before_request():
    if current_user.is_authenticated:
        if current_user.profile:
            current_user.profile.last_seen = datetime.utcnow()
            db.session.commit()
