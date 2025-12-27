from flask import render_template, request, redirect, url_for, flash
from app.db import get_db
from . import bp


@bp.route('/', methods=['GET'])
def index():
    """Lista todos los empleados."""
    db = get_db()
    cur = db.execute('SELECT id, nombre, apellido_paterno, puesto, activo FROM empleados ORDER BY nombre')
    empleados = cur.fetchall()
    return render_template('empleados/index.html', empleados=empleados)


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """Ver detalle de un empleado."""
    db = get_db()
    cur = db.execute('SELECT * FROM empleados WHERE id = ?', (id,))
    empleado = cur.fetchone()
    if empleado is None:
        flash('Empleado no encontrado', 'danger')
        return redirect(url_for('empleados.index'))
    return render_template('empleados/view.html', empleado=empleado)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Crear un nuevo empleado."""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        identificacion = request.form.get('identificacion')
        puesto = request.form.get('puesto')
        departamento = request.form.get('departamento')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        salario = request.form.get('salario', 0)

        db = get_db()
        db.execute(
            '''INSERT INTO empleados 
               (nombre, apellido_paterno, apellido_materno, identificacion, 
                puesto, departamento, email, telefono, salario)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (nombre, apellido_paterno, apellido_materno, identificacion,
             puesto, departamento, email, telefono, salario)
        )
        db.commit()
        flash('Empleado creado exitosamente', 'success')
        return redirect(url_for('empleados.index'))
    
    return render_template('empleados/create.html')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """Editar un empleado."""
    db = get_db()
    cur = db.execute('SELECT * FROM empleados WHERE id = ?', (id,))
    empleado = cur.fetchone()
    
    if empleado is None:
        flash('Empleado no encontrado', 'danger')
        return redirect(url_for('empleados.index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        identificacion = request.form.get('identificacion')
        puesto = request.form.get('puesto')
        departamento = request.form.get('departamento')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        salario = request.form.get('salario')

        db.execute(
            '''UPDATE empleados SET 
               nombre = ?, apellido_paterno = ?, apellido_materno = ?, 
               identificacion = ?, puesto = ?, departamento = ?, 
               email = ?, telefono = ?, salario = ?, 
               updated_at = datetime('now')
               WHERE id = ?''',
            (nombre, apellido_paterno, apellido_materno, identificacion,
             puesto, departamento, email, telefono, salario, id)
        )
        db.commit()
        flash('Empleado actualizado exitosamente', 'success')
        return redirect(url_for('empleados.index'))
    
    return render_template('empleados/edit.html', empleado=empleado)


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    """Eliminar un empleado."""
    db = get_db()
    cur = db.execute('SELECT * FROM empleados WHERE id = ?', (id,))
    empleado = cur.fetchone()
    
    if empleado is None:
        flash('Empleado no encontrado', 'danger')
        return redirect(url_for('empleados.index'))
    
    if request.method == 'POST':
        db.execute('DELETE FROM empleados WHERE id = ?', (id,))
        db.commit()
        flash('Empleado eliminado exitosamente', 'success')
        return redirect(url_for('empleados.index'))
    
    return render_template('empleados/delete.html', empleado=empleado)
