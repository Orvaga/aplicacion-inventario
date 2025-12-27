from flask import render_template, request, redirect, url_for, flash
import sqlite3
import re
from datetime import datetime
from app.db import get_db
from . import bp


@bp.route('/', methods=['GET'])
def index():
    """Lista todos los proveedores."""
    db = get_db()
    cur = db.execute('SELECT id, nombre, razon_social, nit, telefono, producto_servicio, email, direccion FROM proveedores ORDER BY nombre')
    proveedores = cur.fetchall()
    return render_template('proveedores/index.html', proveedores=proveedores)


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """Ver detalle de un proveedor."""
    db = get_db()
    cur = db.execute('SELECT * FROM proveedores WHERE id = ?', (id,))
    proveedor = cur.fetchone()
    if proveedor is None:
        flash('Proveedor no encontrado', 'danger')
        return redirect(url_for('proveedores.index'))
    return render_template('proveedores/view.html', proveedor=proveedor)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Crear un nuevo proveedor."""
    if request.method == 'POST':
        # Basic server-side validation
        errors = []
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            errors.append('El nombre es obligatorio.')

        email = request.form.get('email', '').strip()
        if email:
            # RFC 5322 simplified validation
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                errors.append('El email no tiene formato válido.')

        nit = request.form.get('nit', '').strip()
        if nit and not re.match(r"^[\w\-]{3,30}$", nit):
            errors.append('El NIT no tiene formato válido (solo letras, números, guiones).')

        fecha_registro = request.form.get('fecha_registro') or ''
        if fecha_registro:
            try:
                datetime.strptime(fecha_registro, '%Y-%m-%d')
            except ValueError:
                errors.append('La fecha de registro no es válida (YYYY-MM-DD).')

        notas = request.form.get('notas') or ''
        if len(notas) > 2000:
            errors.append('Las notas no pueden exceder 2000 caracteres.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            # re-render form with previous inputs
            return render_template('proveedores/create.html', **request.form)
        nombre = request.form.get('nombre')
        # rfc removed from schema
        nit = request.form.get('nit')
        razon_social = request.form.get('razon_social')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        contacto = request.form.get('contacto')
        condiciones_pago = request.form.get('condiciones_pago')
        sitio_web = request.form.get('sitio_web')
        producto_servicio = request.form.get('producto_servicio')
        fecha_registro = request.form.get('fecha_registro')
        estado = request.form.get('estado') or 'activo'
        # 'activo' column removed; rely on 'estado' instead

        db = get_db()
        try:
            db.execute(
                '''INSERT INTO proveedores 
                   (nombre, razon_social, nit, direccion, telefono, email, contacto, condiciones_pago, notas, sitio_web, producto_servicio, fecha_registro, estado)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (nombre, razon_social, nit, direccion, telefono, email, contacto, condiciones_pago, request.form.get('notas'), sitio_web, producto_servicio, fecha_registro, estado)
            )
        except sqlite3.IntegrityError as e:
            # Unique constraint failed (e.g., nit)
            flash('No se pudo crear el proveedor: posible NIT duplicado o dato inválido.', 'danger')
            return render_template('proveedores/create.html', **request.form)
        db.commit()
        flash('Proveedor creado exitosamente', 'success')
        return redirect(url_for('proveedores.index'))
    
    return render_template('proveedores/create.html')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """Editar un proveedor."""
    db = get_db()
    cur = db.execute('SELECT * FROM proveedores WHERE id = ?', (id,))
    proveedor = cur.fetchone()
    
    if proveedor is None:
        flash('Proveedor no encontrado', 'danger')
        return redirect(url_for('proveedores.index'))
    
    if request.method == 'POST':
        # Basic server-side validation (same as create)
        errors = []
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            errors.append('El nombre es obligatorio.')

        email = request.form.get('email', '').strip()
        if email:
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                errors.append('El email no tiene formato válido.')

        nit = request.form.get('nit', '').strip()
        if nit and not re.match(r"^[\w\-]{3,30}$", nit):
            errors.append('El NIT no tiene formato válido (solo letras, números, guiones).')

        fecha_registro = request.form.get('fecha_registro') or ''
        if fecha_registro:
            try:
                datetime.strptime(fecha_registro, '%Y-%m-%d')
            except ValueError:
                errors.append('La fecha de registro no es válida (YYYY-MM-DD).')

        notas = request.form.get('notas') or ''
        if len(notas) > 2000:
            errors.append('Las notas no pueden exceder 2000 caracteres.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            # re-render edit form keeping existing proveedor
            return render_template('proveedores/edit.html', proveedor=proveedor, **request.form)
        nombre = request.form.get('nombre')
        # rfc removed from schema
        nit = request.form.get('nit')
        razon_social = request.form.get('razon_social')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        contacto = request.form.get('contacto')
        condiciones_pago = request.form.get('condiciones_pago')
        sitio_web = request.form.get('sitio_web')
        producto_servicio = request.form.get('producto_servicio')
        fecha_registro = request.form.get('fecha_registro')
        estado = request.form.get('estado') or 'activo'
        # 'activo' column removed; rely on 'estado' instead

        db.execute(
            '''UPDATE proveedores SET 
               nombre = ?, razon_social = ?, nit = ?, direccion = ?, telefono = ?, 
               email = ?, contacto = ?, condiciones_pago = ?, notas = ?, sitio_web = ?, producto_servicio = ?, fecha_registro = ?, estado = ?,
               updated_at = datetime('now')
               WHERE id = ?''',
            (nombre, razon_social, nit, direccion, telefono, email, contacto, condiciones_pago, request.form.get('notas'), sitio_web, producto_servicio, fecha_registro, estado, id)
        )
        db.commit()
        flash('Proveedor actualizado exitosamente', 'success')
        return redirect(url_for('proveedores.index'))
    
    return render_template('proveedores/edit.html', proveedor=proveedor)


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    """Eliminar un proveedor."""
    db = get_db()
    cur = db.execute('SELECT * FROM proveedores WHERE id = ?', (id,))
    proveedor = cur.fetchone()
    
    if proveedor is None:
        flash('Proveedor no encontrado', 'danger')
        return redirect(url_for('proveedores.index'))
    
    if request.method == 'POST':
        db.execute('DELETE FROM proveedores WHERE id = ?', (id,))
        db.commit()
        flash('Proveedor eliminado exitosamente', 'success')
        return redirect(url_for('proveedores.index'))
    
    return render_template('proveedores/delete.html', proveedor=proveedor)
