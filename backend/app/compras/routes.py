from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from app.stock import apply_compra_line
from . import bp


@bp.route('/', methods=['GET'])
def index():
    """Lista todas las compras."""
    db = get_db()
    cur = db.execute(
        '''SELECT c.id, c.numero_factura, p.nombre, c.fecha, c.total, c.estado 
           FROM compras c 
           LEFT JOIN proveedores p ON c.proveedor_id = p.id 
           ORDER BY c.fecha DESC LIMIT 100'''
    )
    compras = cur.fetchall()
    return render_template('compras/index.html', compras=compras)


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """Ver detalle de una compra."""
    db = get_db()
    cur = db.execute('SELECT * FROM compras WHERE id = ?', (id,))
    compra = cur.fetchone()
    if compra is None:
        flash('Compra no encontrada', 'danger')
        return redirect(url_for('compras.index'))
    
    cur = db.execute('SELECT * FROM compras_detalle WHERE compra_id = ?', (id,))
    detalles = cur.fetchall()
    # obtener lista de productos para el formulario de detalle
    pcur = db.execute('SELECT id, nombre FROM productos WHERE activo = 1 ORDER BY nombre')
    productos = pcur.fetchall()
    
    return render_template('compras/view.html', compra=compra, detalles=detalles, productos=productos)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Crear una nueva compra."""
    db = get_db()
    
    if request.method == 'POST':
        proveedor_id = request.form.get('proveedor_id')
        numero_factura = request.form.get('numero_factura')
        metodo_pago = request.form.get('metodo_pago')
        
        db.execute(
            '''INSERT INTO compras (proveedor_id, numero_factura, metodo_pago)
               VALUES (?, ?, ?)''',
            (proveedor_id, numero_factura, metodo_pago)
        )
        db.commit()
        flash('Compra creada exitosamente', 'success')
        return redirect(url_for('compras.index'))
    
    # 'proveedores' table now uses 'estado' (activo/inactivo) instead of 'activo' boolean
    cur = db.execute("SELECT id, nombre FROM proveedores WHERE estado = 'activo' ORDER BY nombre")
    proveedores = cur.fetchall()
    
    return render_template('compras/create.html', proveedores=proveedores)


@bp.route('/<int:compra_id>/add_line', methods=['POST'])
def add_line(compra_id):
    """Agregar una línea al detalle de compra y actualizar stock."""
    db = get_db()

    # validar existencia de compra
    cur = db.execute('SELECT id FROM compras WHERE id = ?', (compra_id,))
    compra = cur.fetchone()
    if compra is None:
        flash('Compra no encontrada', 'danger')
        return redirect(url_for('compras.index'))

    try:
        producto_id = int(request.form.get('producto_id'))
        cantidad = float(request.form.get('cantidad') or 0)
    except (TypeError, ValueError):
        flash('Datos de línea inválidos', 'danger')
        return redirect(url_for('compras.view', id=compra_id))

    unidad_medida = request.form.get('unidad_medida')
    precio_unitario = request.form.get('precio_unitario')
    try:
        precio_unitario = float(precio_unitario) if precio_unitario else 0.0
    except ValueError:
        precio_unitario = 0.0

    subtotal = cantidad * precio_unitario

    db.execute(
        '''INSERT INTO compras_detalle (compra_id, producto_id, cantidad, unidad_medida, precio_unitario, subtotal)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (compra_id, producto_id, cantidad, unidad_medida, precio_unitario, subtotal)
    )
    # Actualizar stock y registrar movimiento de almacén
    apply_compra_line(db, compra_id, producto_id, cantidad, unidad_medida)

    # Recalcular totales de la compra
    from app.stock import update_compra_totals
    update_compra_totals(db, compra_id)

    db.commit()
    flash('Línea de compra agregada, stock y totales actualizados', 'success')
    return redirect(url_for('compras.view', id=compra_id))
