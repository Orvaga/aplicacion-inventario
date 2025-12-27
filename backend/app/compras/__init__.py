from flask import Blueprint

bp = Blueprint('compras', __name__, url_prefix='/compras')

from . import routes  # noqa: E402, F401
