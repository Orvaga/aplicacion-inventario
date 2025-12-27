from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from app.stock import apply_venta_line, get_stock
from . import bp


@bp.route('/', methods=['GET'])
def index():
    """Lista todas las ventas."""
    db = get_db()
    cur = db.execute(
        '''SELECT v.id, v.numero_factura, c.nombre, v.fecha, v.total, v.estado 
           FROM ventas v 
           LEFT JOIN clientes c ON v.cliente_id = c.id 
           ORDER BY v.fecha DESC LIMIT 100'''
    )
    ventas = cur.fetchall()
    return render_template('ventas/index.html', ventas=ventas)


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """Ver detalle de una venta."""
    db = get_db()
    cur = db.execute('SELECT * FROM ventas WHERE id = ?', (id,))
    venta = cur.fetchone()
    if venta is None:
        flash('Venta no encontrada', 'danger')
        return redirect(url_for('ventas.index'))
    
    cur = db.execute('SELECT * FROM ventas_detalle WHERE venta_id = ?', (id,))
    detalles = cur.fetchall()
    # obtener productos y stock para el formulario
    pcur = db.execute(
        '''SELECT p.id, p.nombre, COALESCE(s.cantidad, 0) as cantidad
           FROM productos p
           LEFT JOIN stock s ON p.id = s.producto_id
           WHERE p.activo = 1
           ORDER BY p.nombre'''
    )
    productos = pcur.fetchall()
    
    return render_template('ventas/view.html', venta=venta, detalles=detalles, productos=productos)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Crear una nueva venta."""
    db = get_db()
    
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        numero_factura = request.form.get('numero_factura')
        metodo_pago = request.form.get('metodo_pago')
        
        db.execute(
            '''INSERT INTO ventas (cliente_id, numero_factura, metodo_pago)
               VALUES (?, ?, ?)''',
            (cliente_id, numero_factura, metodo_pago)
        )
        db.commit()
        flash('Venta creada exitosamente', 'success')
        return redirect(url_for('ventas.index'))
    
    cur = db.execute('SELECT id, nombre FROM clientes WHERE activo = 1 ORDER BY nombre')
    clientes = cur.fetchall()
    
    return render_template('ventas/create.html', clientes=clientes)


@bp.route('/<int:venta_id>/add_line', methods=['POST'])
def add_line(venta_id):
    """Agregar una línea al detalle de venta y actualizar stock."""
    db = get_db()

    # validar existencia de venta
    cur = db.execute('SELECT id FROM ventas WHERE id = ?', (venta_id,))
    venta = cur.fetchone()
    if venta is None:
        flash('Venta no encontrada', 'danger')
        return redirect(url_for('ventas.index'))

    try:
        producto_id = int(request.form.get('producto_id'))
        cantidad = float(request.form.get('cantidad') or 0)
    except (TypeError, ValueError):
        flash('Datos de línea inválidos', 'danger')
        return redirect(url_for('ventas.view', id=venta_id))

    # Comprobar stock disponible antes de insertar la línea
    disponible = get_stock(db, producto_id)
    if cantidad > disponible:
        flash(f'Stock insuficiente para el producto seleccionado (disponible: {disponible})', 'danger')
        return redirect(url_for('ventas.view', id=venta_id))

    unidad_medida = request.form.get('unidad_medida')
    precio_unitario = request.form.get('precio_unitario')
    try:
        precio_unitario = float(precio_unitario) if precio_unitario else 0.0
    except ValueError:
        precio_unitario = 0.0

    subtotal = cantidad * precio_unitario

    db.execute(
        '''INSERT INTO ventas_detalle (venta_id, producto_id, cantidad, unidad_medida, precio_unitario, subtotal)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (venta_id, producto_id, cantidad, unidad_medida, precio_unitario, subtotal)
    )
    # Actualizar stock y registrar movimiento de almacén (salida)
    apply_venta_line(db, venta_id, producto_id, cantidad, unidad_medida)

    # Recalcular totales de la venta
    from app.stock import update_venta_totals
    update_venta_totals(db, venta_id)

    db.commit()
    flash('Línea de venta agregada, stock y totales actualizados', 'success')
    return redirect(url_for('ventas.view', id=venta_id))
