from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from app.stock import record_almacen, update_stock
from . import bp


@bp.route('/', methods=['GET'])
def index():
    """Lista movimientos de almacén."""
    db = get_db()
    cur = db.execute(
        '''SELECT a.id, a.tipo_movimiento, p.nombre, a.cantidad, a.fecha 
           FROM almacen a 
           LEFT JOIN productos p ON a.producto_id = p.id 
           ORDER BY a.fecha DESC LIMIT 100'''
    )
    movimientos = cur.fetchall()
    return render_template('almacen/index.html', movimientos=movimientos)


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """Ver detalle de un movimiento."""
    db = get_db()
    cur = db.execute('SELECT * FROM almacen WHERE id = ?', (id,))
    movimiento = cur.fetchone()
    if movimiento is None:
        flash('Movimiento no encontrado', 'danger')
        return redirect(url_for('almacen.index'))
    return render_template('almacen/view.html', movimiento=movimiento)


@bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Registrar un movimiento de almacén."""
    db = get_db()
    
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        tipo_movimiento = request.form.get('tipo_movimiento')
        cantidad = request.form.get('cantidad')
        motivo = request.form.get('motivo')
        
        try:
            producto_id_i = int(producto_id)
            cantidad_f = float(cantidad)
        except (TypeError, ValueError):
            flash('Datos inválidos para movimiento', 'danger')
            return redirect(url_for('almacen.index'))

        # registrar movimiento y actualizar stock
        record_almacen(db, producto_id_i, tipo_movimiento, cantidad_f, 'manual', None, None, None)
        if tipo_movimiento == 'entrada':
            update_stock(db, producto_id_i, cantidad_f)
        elif tipo_movimiento == 'salida':
            update_stock(db, producto_id_i, -abs(cantidad_f))
        else:
            # ajuste: aplicar la cantidad tal cual (puede ser positiva/negativa)
            update_stock(db, producto_id_i, cantidad_f)

        db.commit()
        flash('Movimiento registrado y stock actualizado', 'success')
        return redirect(url_for('almacen.index'))
    
    cur = db.execute('SELECT id, nombre FROM productos WHERE activo = 1 ORDER BY nombre')
    productos = cur.fetchall()
    
    return render_template('almacen/registrar.html', productos=productos)
