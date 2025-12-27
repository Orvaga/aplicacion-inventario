"""Validación para `proveedores` (script, no pytest). 
Este script recrea la DB y prueba validaciones de servidor del blueprint proveedores.
"""
import sqlite3
from pathlib import Path
import subprocess
import shutil
import os
from app import create_app

BASE = Path(__file__).parent
DB_PATH = BASE / "database.db"
BACKUP_PATH = BASE / "database.db.bak"


def recreate_db():
    if DB_PATH.exists():
        if not BACKUP_PATH.exists():
            shutil.copy2(DB_PATH, BACKUP_PATH)
        os.remove(DB_PATH)
    subprocess.check_call(['python', str(BASE / 'create_database.py')], cwd=str(BASE))


def count_proveedores(nombre):
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.execute('SELECT COUNT(*) as c FROM proveedores WHERE nombre = ?', (nombre,))
    c = cur.fetchone()['c']
    conn.close()
    return c


def run():
    print('==> Preparando DB y app')
    recreate_db()
    app = create_app({'TESTING': True})
    app.testing = True

    with app.test_client() as client:
        # 1) Intentar insertar sin nombre (debería fallar / no insertar)
        data_invalid = {
            'nombre': '',
            'nit': 'NIT12345',
            'email': 'bad-email',
            'producto_servicio': 'Suministros',
            'estado': 'activo'
        }
        resp = client.post('/proveedores/create', data=data_invalid, follow_redirects=True)
        print('POST invalid -> status', resp.status_code)
        assert count_proveedores('') == 0, 'No debe insertarse proveedor con nombre vacío'

        # 2) Insertar con email inválido (debe fallar)
        data_invalid_email = {
            'nombre': 'Prov Sin Email Valido',
            'nit': 'NITX',
            'email': 'notanemail',
            'producto_servicio': 'Suministros',
            'estado': 'activo'
        }
        resp = client.post('/proveedores/create', data=data_invalid_email, follow_redirects=True)
        print('POST invalid-email -> status', resp.status_code)
        assert count_proveedores('Prov Sin Email Valido') == 0, 'No debe insertarse proveedor con email inválido'

        # 3) Insertar con fecha inválida (debe fallar)
        data_invalid_date = {
            'nombre': 'Prov Fecha Mala',
            'nit': 'NITX',
            'email': 'valido@test.com',
            'fecha_registro': '2025-99-99',
            'producto_servicio': 'Suministros',
            'estado': 'activo'
        }
        resp = client.post('/proveedores/create', data=data_invalid_date, follow_redirects=True)
        print('POST invalid-date -> status', resp.status_code)
        assert count_proveedores('Prov Fecha Mala') == 0, 'No debe insertarse proveedor con fecha inválida'

        # 4) Insertar proveedor válido (debe insertar)
        data_ok = {
            'nombre': 'Proveedor Valido',
            'nit': 'NIT-VALIDO-001',
            'razon_social': 'Proveedor Valido S.A.',
            'direccion': 'Dir 1',
            'telefono': '555-1212',
            'email': 'contacto@empresa.test',
            'contacto': 'Contacto',
            'condiciones_pago': '30 dias',
            'sitio_web': 'https://empresa.test',
            'producto_servicio': 'Servicios',
            'fecha_registro': '2025-11-25',
            'estado': 'activo',
            'notas': 'Test valido'
        }
        resp = client.post('/proveedores/create', data=data_ok, follow_redirects=True)
        print('POST ok -> status', resp.status_code)
        assert count_proveedores('Proveedor Valido') == 1, 'Proveedor válido debe insertarse'

    print('==> Validaciones OK')


if __name__ == '__main__':
    run()
