from datetime import datetime

from app.db import get_db


def _now():
    return datetime.utcnow().isoformat(sep=' ', timespec='seconds')


def record_almacen(db, producto_id, tipo_movimiento, cantidad, referencia, referencia_id=None, unidad_medida=None, motivo=None, usuario_id=None):
    db.execute(
        '''INSERT INTO almacen (producto_id, tipo_movimiento, cantidad, unidad_medida, referencia, referencia_id, motivo, usuario_id, fecha)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (producto_id, tipo_movimiento, cantidad, unidad_medida, referencia, referencia_id, motivo, usuario_id, _now())
    )


def update_stock(db, producto_id, cantidad, ubicacion=None):
    """Ajusta la tabla `stock` sumando `cantidad` (puede ser negativa).

    Si existe una fila para la combinación producto+ubicación, la actualiza; si no, la crea.
    """
    cur = db.execute(
        'SELECT id, cantidad FROM stock WHERE producto_id = ? AND (ubicacion = ? OR (? IS NULL AND ubicacion IS NULL))',
        (producto_id, ubicacion, ubicacion)
    )
    row = cur.fetchone()
    now = _now()
    if row:
        new_cantidad = row['cantidad'] + cantidad
        db.execute(
            'UPDATE stock SET cantidad = ?, ultimo_movimiento = ?, updated_at = ? WHERE id = ?',
            (new_cantidad, now, now, row['id'])
        )
    else:
        db.execute(
            'INSERT INTO stock (producto_id, ubicacion, cantidad, ultimo_movimiento, updated_at) VALUES (?, ?, ?, ?, ?)',
            (producto_id, ubicacion, cantidad, now, now)
        )


def apply_compra_line(db, compra_id, producto_id, cantidad, unidad_medida=None, usuario_id=None):
    """Aplica una línea de compra: registra en `almacen` como entrada y suma en `stock`."""
    # registrar movimiento de entrada
    record_almacen(db, producto_id, 'entrada', cantidad, 'compra', compra_id, unidad_medida, usuario_id)
    # actualizar stock (aumenta)
    update_stock(db, producto_id, cantidad)


def apply_venta_line(db, venta_id, producto_id, cantidad, unidad_medida=None, usuario_id=None):
    """Aplica una línea de venta: registra en `almacen` como salida y resta del `stock`."""
    # registrar movimiento de salida
    record_almacen(db, producto_id, 'salida', cantidad, 'venta', venta_id, unidad_medida, usuario_id)
    # actualizar stock (disminuye)
    update_stock(db, producto_id, -abs(cantidad))


def update_compra_totals(db, compra_id):
    """Recalcula subtotal/total de la compra a partir de compras_detalle."""
    cur = db.execute('SELECT SUM(subtotal) as s FROM compras_detalle WHERE compra_id = ?', (compra_id,))
    row = cur.fetchone()
    subtotal = row['s'] if row and row['s'] is not None else 0.0
    # por ahora no calculamos impuestos ni descuentos
    total = subtotal
    db.execute('UPDATE compras SET subtotal = ?, total = ?, updated_at = ? WHERE id = ?', (subtotal, total, _now(), compra_id))


def update_venta_totals(db, venta_id):
    """Recalcula subtotal/total de la venta a partir de ventas_detalle."""
    cur = db.execute('SELECT SUM(subtotal) as s FROM ventas_detalle WHERE venta_id = ?', (venta_id,))
    row = cur.fetchone()
    subtotal = row['s'] if row and row['s'] is not None else 0.0
    total = subtotal
    db.execute('UPDATE ventas SET subtotal = ?, total = ?, updated_at = ? WHERE id = ?', (subtotal, total, _now(), venta_id))


def get_stock(db, producto_id, ubicacion=None):
    """Devuelve la cantidad en stock para un producto (por ubicación opcional)."""
    cur = db.execute('SELECT cantidad FROM stock WHERE producto_id = ? AND (ubicacion = ? OR (? IS NULL AND ubicacion IS NULL))', (producto_id, ubicacion, ubicacion))
    row = cur.fetchone()
    return float(row['cantidad']) if row and row['cantidad'] is not None else 0.0
