import sys
import os
from pathlib import Path
from flask import Flask

from app import create_app
# Añadir la raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
