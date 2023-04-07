from flask import Blueprint

# create instance of 'auth' blueprint
bp = Blueprint("auth", __name__, url_prefix="/auth")

# import blueprint's routes
from . import routes  # noqa
