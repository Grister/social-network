from flask import Blueprint

# create instance of 'auth' blueprint
bp = Blueprint("main", __name__, url_prefix="/")

# import blueprint's routes
from . import routes  # noqa
