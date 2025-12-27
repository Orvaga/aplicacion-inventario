import sys
import os
from pathlib import Path

# Añadir el directorio backend al path ANTES de importar
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
