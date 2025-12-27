from flask import Blueprint

bp = Blueprint('almacen', __name__, url_prefix='/almacen')

from . import routes  # noqa: E402, F401
