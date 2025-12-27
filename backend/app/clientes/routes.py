from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from . import bp


@bp.route('/', methods=['GET'])
def index():
    """Lista todos los clientes."""
    db = get_db()
    cur = db.execute('SELECT id, nombre, tipo, email, activo FROM clientes ORDER BY nombre')
    clientes = cur.fetchall()
    return render_template('clientes/index.html', clientes=clientes)


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """Ver detalle de un cliente."""
    db = get_db()
    cur = db.execute('SELECT * FROM clientes WHERE id = ?', (id,))
    cliente = cur.fetchone()
    if cliente is None:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('clientes.index'))
    return render_template('clientes/view.html', cliente=cliente)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Crear un nuevo cliente."""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        rfc = request.form.get('rfc')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        credito_limite = request.form.get('credito_limite', 0)

        db = get_db()
        db.execute(
            '''INSERT INTO clientes 
               (nombre, tipo, rfc, direccion, telefono, email, credito_limite)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (nombre, tipo, rfc, direccion, telefono, email, credito_limite)
        )
        db.commit()
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('clientes.index'))
    
    return render_template('clientes/create.html')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """Editar un cliente."""
    db = get_db()
    cur = db.execute('SELECT * FROM clientes WHERE id = ?', (id,))
    cliente = cur.fetchone()
    
    if cliente is None:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('clientes.index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        rfc = request.form.get('rfc')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        credito_limite = request.form.get('credito_limite')

        db.execute(
            '''UPDATE clientes SET 
               nombre = ?, tipo = ?, rfc = ?, direccion = ?, 
               telefono = ?, email = ?, credito_limite = ?, 
               updated_at = datetime('now')
               WHERE id = ?''',
            (nombre, tipo, rfc, direccion, telefono, email, credito_limite, id)
        )
        db.commit()
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('clientes.index'))
    
    return render_template('clientes/edit.html', cliente=cliente)


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    """Eliminar un cliente."""
    db = get_db()
    cur = db.execute('SELECT * FROM clientes WHERE id = ?', (id,))
    cliente = cur.fetchone()
    
    if cliente is None:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('clientes.index'))
    
    if request.method == 'POST':
        db.execute('DELETE FROM clientes WHERE id = ?', (id,))
        db.commit()
        flash('Cliente eliminado exitosamente', 'success')
        return redirect(url_for('clientes.index'))
    
    return render_template('clientes/delete.html', cliente=cliente)
