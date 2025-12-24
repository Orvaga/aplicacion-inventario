import sys
from pathlib import Path
from flask import Flask
# Añadir la raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app import create_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080, use_reloader=False)
