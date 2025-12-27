"""Test flow: crea la DB, crea un proveedor via Flask test client y verifica registro en DB.

Ejecutar desde la raíz del repo:
  python backend/test_proveedores_flow.py
"""
import sqlite3
from pathlib import Path
import shutil
import subprocess
import os
from app import create_app

BASE = Path(__file__).parent
DB_PATH = BASE / "database.db"
BACKUP_PATH = BASE / "database.db.bak"

# 1) Recreate DB schema
print('==> Preparando DB (respaldar y recrear)')
if DB_PATH.exists():
    if not BACKUP_PATH.exists():
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print(f'==> Backup creado en: {BACKUP_PATH}')
    else:
        print(f'==> Backup previo detectado: {BACKUP_PATH}')
    # eliminar DB para forzar recreación con DDL actualizado
    try:
        os.remove(DB_PATH)
        print('==> DB previa eliminada para recrear desde esquema')
    except OSError:
        pass

print('==> Creando/actualizando DB desde esquema')
subprocess.check_call(['python', str(BASE / 'create_database.py')], cwd=str(BASE))

# Make a backup of DB prior to testing (if there is not already a bak)
if DB_PATH.exists():
    if not BACKUP_PATH.exists():
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print(f'==> Backup creado en: {BACKUP_PATH}')
    else:
        print(f'==> Backup previo detectado: {BACKUP_PATH}')

# 2) Launch Flask app in testing mode
app = create_app({'TESTING': True})
app.testing = True

with app.test_client() as client:
    data = {
        'nombre': 'Proveedor Test',
        'nit': 'NIT123456',
        'razon_social': 'Proveedor Test S.A.',
        'direccion': 'Calle Test 123',
        'telefono': '555-0000',
        'email': 'prueba@example.test',
        'contacto': 'Juan Tester',
        'condiciones_pago': '30 dias',
        'sitio_web': 'https://example.test',
        'producto_servicio': 'Suministros',
        'fecha_registro': '2025-11-25',
        'estado': 'activo',
        'notas': 'Nota automatizada de prueba estamos probando',
    }

    print('==> Enviando POST a /proveedores/create')
    resp = client.post('/proveedores/create', data=data, follow_redirects=True)
    print(f'==> POST -> status code: {resp.status_code}')

# 3) Verify record in DB
conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cur = conn.execute('SELECT * FROM proveedores WHERE nombre = ?', ('Proveedor Test',))
row = cur.fetchone()
if row:
    print('==> Registro encontrado:')
    for k in row.keys():
        print(f'  {k}: {row[k]}')
else:
    print('==> No se encontró el registro — algo falló')

conn.close()

# 4) Restore DB from bak if present (optional) — we will leave as-is but we can restore if needed
print('==> Fin del script')
