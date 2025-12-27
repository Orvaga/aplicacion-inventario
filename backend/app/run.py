import sys
from pathlib import Path
from flask import Flask
# Añadir la raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from __init__ import create_app
# from .app.__init__ import create_app
# from . import db

app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
