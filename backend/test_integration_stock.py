"""
Script de integración para verificar que al agregar líneas de compra/venta se actualiza la tabla `stock`.
Ejecutar: python test_integration_stock.py
"""
import sys
sys.path.insert(0, 'd:/huilawed/aplicacion_app')
from backend.app import create_app
from app.db import get_db
import time

app = create_app()

errors = []

with app.app_context():
    db = get_db()
    # crear un producto de prueba
    sku = f"TESTSKU_{int(time.time()*1000)}"
    cur = db.execute("INSERT INTO productos (sku, nombre, precio_venta, activo) VALUES (?, ?, ?, 1)", (sku, 'Producto Test', 10.0))
    db.commit()
    prod_id = db.execute('SELECT id FROM productos WHERE sku = ?', (sku,)).fetchone()['id']

    # crear una compra
    db.execute("INSERT INTO compras (proveedor_id, numero_factura) VALUES (?, ?)", (1, 'F-TEST'))
    db.commit()
    compra_id = db.execute('SELECT id FROM compras WHERE numero_factura = ?', ('F-TEST',)).fetchone()['id']

    # agregar línea de compra usando la función interna (simula endpoint)
    from app.stock import apply_compra_line, update_compra_totals
    apply_compra_line(db, compra_id, prod_id, 5)
    update_compra_totals(db, compra_id)
    db.commit()

    # comprobar stock
    row = db.execute('SELECT cantidad FROM stock WHERE producto_id = ?', (prod_id,)).fetchone()
    if not row or row['cantidad'] != 5:
        errors.append(f"Stock incorrecto después de compra: esperado 5, obtenido {row['cantidad'] if row else 'None'}")

    # crear una venta
    db.execute("INSERT INTO clientes (nombre, activo) VALUES (?, 1)", ('Cliente Test',))
    db.commit()
    cliente_id = db.execute('SELECT id FROM clientes WHERE nombre = ?', ('Cliente Test',)).fetchone()['id']
    db.execute("INSERT INTO ventas (cliente_id, numero_factura) VALUES (?, ?)", (cliente_id, 'V-TEST'))
    db.commit()
    venta_id = db.execute('SELECT id FROM ventas WHERE numero_factura = ?', ('V-TEST',)).fetchone()['id']

    from app.stock import apply_venta_line, update_venta_totals
    apply_venta_line(db, venta_id, prod_id, 2)
    update_venta_totals(db, venta_id)
    db.commit()

    row2 = db.execute('SELECT cantidad FROM stock WHERE producto_id = ?', (prod_id,)).fetchone()
    if not row2 or row2['cantidad'] != 3:
        errors.append(f"Stock incorrecto después de venta: esperado 3, obtenido {row2['cantidad'] if row2 else 'None'}")

if errors:
    print("FALLÓ:\n" + "\n".join(errors))
    sys.exit(1)
else:
    print("OK: stock actualizado correctamente tras compra y venta")
    sys.exit(0)
