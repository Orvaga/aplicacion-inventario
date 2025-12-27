import sqlite3
from pathlib import Path
import pytest
from app import create_app
import os


@pytest.fixture
def app(tmp_path):
    # Create a temporary DB for tests and initialize schema
    tmp_db = tmp_path / "test_database.db"
    sql_path = Path(__file__).parent / "database_schema.sql"
    sql = sql_path.read_text(encoding="utf-8")

    conn = sqlite3.connect(str(tmp_db))
    conn.executescript(sql)
    conn.commit()
    conn.close()

    app = create_app({'TESTING': True})
    # override DATABASE after app creation so our fixture uses an isolated DB
    app.config['DATABASE'] = str(tmp_db)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def db_count(db_path, nombre):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.execute('SELECT COUNT(*) AS c FROM proveedores WHERE nombre = ?', (nombre,))
    c = cur.fetchone()['c']
    conn.close()
    return c


def test_create_missing_nombre(client, tmp_path, app):
    db_path = Path(app.config['DATABASE'])
    data = {
        'nombre': '',
        'nit': 'NIT123',
        'email': 'valid@test.com',
        'producto_servicio': 'Suministros',
        'estado': 'activo'
    }
    resp = client.post('/proveedores/create', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert db_count(db_path, '') == 0


def test_create_invalid_email(client, tmp_path, app):
    db_path = Path(app.config['DATABASE'])
    data = {
        'nombre': 'Proveedor No Email',
        'nit': 'NIT123',
        'email': 'not-an-email',
        'producto_servicio': 'Suministros',
        'estado': 'activo'
    }
    resp = client.post('/proveedores/create', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert db_count(db_path, 'Proveedor No Email') == 0


def test_create_invalid_fecha(client, tmp_path, app):
    db_path = Path(app.config['DATABASE'])
    data = {
        'nombre': 'Proveedor Fecha Mala',
        'nit': 'NIT123',
        'email': 'ok@test.com',
        'fecha_registro': '2025-99-99',
        'producto_servicio': 'Suministros',
        'estado': 'activo'
    }
    resp = client.post('/proveedores/create', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert db_count(db_path, 'Proveedor Fecha Mala') == 0


def test_create_ok(client, tmp_path, app):
    db_path = Path(app.config['DATABASE'])
    data = {
        'nombre': 'Proveedor Valido',
        'nit': 'NIT-VALID',
        'razon_social': 'Raz S.A.',
        'email': 'contact@valido.test',
        'producto_servicio': 'Servicios',
        'fecha_registro': '2025-11-25',
        'estado': 'activo',
        'notas': 'Prueba ok'
    }
    resp = client.post('/proveedores/create', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert db_count(db_path, 'Proveedor Valido') == 1


def test_duplicate_nit(client, tmp_path, app):
    db_path = Path(app.config['DATABASE'])
    data = {
        'nombre': 'Proveedor Uno',
        'nit': 'NIT-DUP-001',
        'email': 'uno@test.com',
        'producto_servicio': 'Suministros',
        'estado': 'activo'
    }
    resp = client.post('/proveedores/create', data=data, follow_redirects=True)
    assert resp.status_code == 200
    # Second insert same NIT should not create a new record
    data2 = data.copy()
    data2['nombre'] = 'Proveedor Dos'
    resp = client.post('/proveedores/create', data=data2, follow_redirects=True)
    assert resp.status_code == 200
    assert db_count(db_path, 'Proveedor Uno') == 1
    assert db_count(db_path, 'Proveedor Dos') == 0


def create_provider_and_get_id(client, db_path, nombre='Proveedor Para CRUD'):
    data = {
        'nombre': nombre,
        'nit': 'NIT-CRUD-001',
        'email': 'crud@test.com',
        'producto_servicio': 'Servicios',
        'estado': 'activo'
    }
    client.post('/proveedores/create', data=data, follow_redirects=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.execute('SELECT id FROM proveedores WHERE nombre = ?', (nombre,))
    row = cur.fetchone()
    conn.close()
    return row['id'] if row else None


def test_index_and_view_detail(client, tmp_path, app):
    db_path = Path(app.config['DATABASE'])
    # create two providers
    client.post('/proveedores/create', data={'nombre': 'Prov A', 'nit': 'NITA', 'email': 'a@test.com', 'producto_servicio': 'S1', 'estado': 'activo'}, follow_redirects=True)
    client.post('/proveedores/create', data={'nombre': 'Prov B', 'nit': 'NITB', 'email': 'b@test.com', 'producto_servicio': 'S2', 'estado': 'activo'}, follow_redirects=True)

    # index page should list both
    resp = client.get('/proveedores/')
    html = resp.get_data(as_text=True)
    assert 'Prov A' in html
    assert 'Prov B' in html

    # view detail for Prov A
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.execute('SELECT id FROM proveedores WHERE nombre = ?', ('Prov A',))
    id_a = cur.fetchone()['id']
    conn.close()
    resp = client.get(f'/proveedores/{id_a}')
    html = resp.get_data(as_text=True)
    assert 'Prov A' in html
    assert 'S1' in html


def test_edit_valid_and_invalid(client, tmp_path, app):
    db_path = Path(app.config['DATABASE'])
    pid = create_provider_and_get_id(client, db_path, nombre='Prov Edit')
    assert pid is not None

    # valid edit: change nombre + email
    data_ok = {'nombre': 'Prov Edit Mod', 'email': 'edit@test.com', 'nit': 'NIT-EDIT-01', 'producto_servicio': 'Servicios', 'estado': 'activo'}
    resp = client.post(f'/proveedores/{pid}/edit', data=data_ok, follow_redirects=True)
    assert resp.status_code == 200
    # DB reflect changes
    conn = sqlite3.connect(str(db_path)); conn.row_factory = sqlite3.Row
    cur = conn.execute('SELECT nombre, email FROM proveedores WHERE id = ?', (pid,))
    row = cur.fetchone(); conn.close()
    assert row['nombre'] == 'Prov Edit Mod'
    assert row['email'] == 'edit@test.com'

    # invalid edit: empty nombre should not change
    data_invalid = {'nombre': '', 'email': 'bad@test.com', 'nit': 'NIT-EDIT-01', 'producto_servicio': 'Servicios', 'estado': 'activo'}
    resp = client.post(f'/proveedores/{pid}/edit', data=data_invalid, follow_redirects=True)
    assert resp.status_code == 200
    conn = sqlite3.connect(str(db_path)); conn.row_factory = sqlite3.Row
    cur = conn.execute('SELECT nombre FROM proveedores WHERE id = ?', (pid,))
    row = cur.fetchone(); conn.close()
    assert row['nombre'] == 'Prov Edit Mod'


def test_delete_provider(client, tmp_path, app):
    db_path = Path(app.config['DATABASE'])
    pid = create_provider_and_get_id(client, db_path, nombre='Prov Delete')
    assert pid is not None

    # validate page exists
    resp = client.get(f'/proveedores/{pid}/delete')
    assert resp.status_code == 200

    # perform delete
    resp = client.post(f'/proveedores/{pid}/delete', follow_redirects=True)
    assert resp.status_code == 200
    # ensure removal
    conn = sqlite3.connect(str(db_path)); conn.row_factory = sqlite3.Row
    cur = conn.execute('SELECT COUNT(*) AS c FROM proveedores WHERE id = ?', (pid,))
    c = cur.fetchone()['c']; conn.close()
    assert c == 0
