import sys
from pathlib import Path

# Lista de archivos routes.py a actualizar
files_to_update = [
    'd:/huilawed/aplicacion_app/backend/app/proveedores/routes.py',
    'd:/huilawed/aplicacion_app/backend/app/compras/routes.py',
    'd:/huilawed/aplicacion_app/backend/app/ventas/routes.py',
    'd:/huilawed/aplicacion_app/backend/app/almacen/routes.py',
    'd:/huilawed/aplicacion_app/backend/app/clientes/routes.py',
    'd:/huilawed/aplicacion_app/backend/app/empleados/routes.py',
]

for fpath in files_to_update:
    p = Path(fpath)
    content = p.read_text(encoding='utf-8')
    # Reemplazar el import incorrecto
    updated = content.replace('from ...db import get_db', 'from app.db import get_db')
    p.write_text(updated, encoding='utf-8')
    print(f"Actualizado: {p.name}")

print("✓ Todos los imports actualizados correctamente")
