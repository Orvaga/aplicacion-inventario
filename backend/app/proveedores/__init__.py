from flask import Blueprint

bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

from . import routes  # noqa: E402, F401
