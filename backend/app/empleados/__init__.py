from flask import Blueprint

bp = Blueprint('empleados', __name__, url_prefix='/empleados')

from . import routes  # noqa: E402, F401
