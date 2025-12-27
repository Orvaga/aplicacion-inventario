from flask import render_template
from app.db import get_db
from . import bp


@bp.route('/')
def index():
    """Dashboard principal."""
    return render_template('index.html')
