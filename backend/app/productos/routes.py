from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from . import bp


@bp.route('/', methods=['GET'])
def index():
    """Lista todos los productos."""
    db = get_db()
    cur = db.execute('SELECT id, sku, nombre, categoria, precio_venta FROM productos ORDER BY nombre')
    productos = cur.fetchall()
    return render_template('productos/index.html', productos=productos)


@bp.route('/grid', methods=['GET'])
def grid():
    """Fragmento simple: grilla de productos para carga AJAX desde el menú."""
    db = get_db()
    cur = db.execute('SELECT id, sku, nombre, categoria, precio_venta FROM productos ORDER BY nombre')
    productos = cur.fetchall()
    return render_template('productos/grid.html', productos=productos)


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """Ver detalle de un producto."""
    db = get_db()
    cur = db.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cur.fetchone()
    if producto is None:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos.index'))
    return render_template('productos/view.html', producto=producto)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Crear un nuevo producto."""
    if request.method == 'POST':
        sku = request.form.get('sku')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        unidad_medida = request.form.get('unidad_medida')
        precio_costo = request.form.get('precio_costo', 0)
        precio_venta = request.form.get('precio_venta', 0)
        stock_minimo = request.form.get('stock_minimo', 0)

        db = get_db()
        try:
            db.execute(
                '''INSERT INTO productos 
                   (sku, nombre, descripcion, categoria, unidad_medida, 
                    precio_costo, precio_venta, stock_minimo)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (sku, nombre, descripcion, categoria, unidad_medida,
                 precio_costo, precio_venta, stock_minimo)
            )
            db.commit()
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('productos.index'))
        except db.IntegrityError:
            flash('El SKU ya existe', 'danger')
    
    return render_template('productos/create.html')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """Editar un producto."""
    db = get_db()
    cur = db.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cur.fetchone()
    
    if producto is None:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos.index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        categoria = request.form.get('categoria')
        unidad_medida = request.form.get('unidad_medida')
        precio_costo = request.form.get('precio_costo')
        precio_venta = request.form.get('precio_venta')
        stock_minimo = request.form.get('stock_minimo')

        db.execute(
            '''UPDATE productos SET 
               nombre = ?, descripcion = ?, categoria = ?, 
               unidad_medida = ?, precio_costo = ?, precio_venta = ?, 
               stock_minimo = ?, updated_at = datetime('now')
               WHERE id = ?''',
            (nombre, descripcion, categoria, unidad_medida, 
             precio_costo, precio_venta, stock_minimo, id)
        )
        db.commit()
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('productos.index'))
    
    return render_template('productos/edit.html', producto=producto)


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    """Eliminar un producto."""
    db = get_db()
    cur = db.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cur.fetchone()
    
    if producto is None:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos.index'))
    
    if request.method == 'POST':
        db.execute('DELETE FROM productos WHERE id = ?', (id,))
        db.commit()
        flash('Producto eliminado exitosamente', 'success')
        return redirect(url_for('productos.index'))
    
    return render_template('productos/delete.html', producto=producto)
