"""
Script para insertar 20 registros de prueba en cada tabla/módulo de la aplicación.

Uso:
    python backend/seed_data.py
"""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random

BASE = Path(__file__).parent
DB_PATH = BASE / "database.db"


def get_db_connection():
    """Conecta a la base de datos."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def seed_proveedores(conn):
    """Inserta 20 proveedores de prueba."""
    print("Insertando 20 proveedores...")
    
    proveedores = [
        ("Distribuidora ABC", "Distribuidora ABC S.A.", "NIT001", "Calle Principal 123", "555-0001", "abc@example.com", "Juan Pérez", "30 días", "Proveedor confiable", "https://abc.com", "Distribución", "2024-01-15", "activo"),
        ("Suministros XYZ", "Suministros XYZ Ltda.", "NIT002", "Av. Comercial 456", "555-0002", "xyz@example.com", "María González", "Contado", "Entrega rápida", "https://xyz.com", "Suministros", "2024-02-20", "activo"),
        ("Servicios Técnicos Pro", "STP S.A.", "NIT003", "Calle Técnica 789", "555-0003", "stp@example.com", "Carlos Rodríguez", "15 días", "Servicio técnico especializado", "https://stp.com", "Servicios", "2024-03-10", "activo"),
        ("Materiales Construcción", "Materiales MC S.A.", "NIT004", "Zona Industrial 101", "555-0004", "mc@example.com", "Ana Martínez", "45 días", "Materiales de construcción", "https://mc.com", "Construcción", "2024-04-05", "activo"),
        ("Equipos Industriales", "Equipos EI S.A.", "NIT005", "Parque Industrial 202", "555-0005", "ei@example.com", "Luis Sánchez", "60 días", "Equipos pesados", "https://ei.com", "Equipos", "2024-05-12", "activo"),
        ("Insumos Médicos", "Insumos Médicos IM S.A.", "NIT006", "Av. Salud 303", "555-0006", "im@example.com", "Patricia López", "30 días", "Insumos hospitalarios", "https://im.com", "Salud", "2024-06-18", "activo"),
        ("Papelería y Oficina", "Papelería PO S.A.", "NIT007", "Centro Comercial 404", "555-0007", "po@example.com", "Roberto Díaz", "Contado", "Artículos de oficina", "https://po.com", "Oficina", "2024-07-22", "activo"),
        ("Alimentos y Bebidas", "Alimentos AB S.A.", "NIT008", "Mercado Central 505", "555-0008", "ab@example.com", "Carmen Ruiz", "7 días", "Productos alimenticios", "https://ab.com", "Alimentos", "2024-08-30", "activo"),
        ("Transporte y Logística", "Transporte TL S.A.", "NIT009", "Terminal Transporte 606", "555-0009", "tl@example.com", "Fernando Torres", "30 días", "Servicios de transporte", "https://tl.com", "Transporte", "2024-09-14", "activo"),
        ("Tecnología Informática", "Tech IT S.A.", "NIT010", "Zona Tecnológica 707", "555-0010", "tech@example.com", "Laura Vega", "Contado", "Equipos informáticos", "https://tech.com", "Tecnología", "2024-10-08", "activo"),
        ("Químicos Industriales", "Químicos QI S.A.", "NIT011", "Zona Industrial 808", "555-0011", "qi@example.com", "Miguel Castro", "45 días", "Productos químicos", "https://qi.com", "Químicos", "2024-11-25", "activo"),
        ("Textiles y Confección", "Textiles TC S.A.", "NIT012", "Calle Moda 909", "555-0012", "tc@example.com", "Sandra Morales", "30 días", "Telas y confecciones", "https://tc.com", "Textiles", "2024-12-01", "activo"),
        ("Herramientas y Ferretería", "Herramientas HF S.A.", "NIT013", "Av. Ferretería 1010", "555-0013", "hf@example.com", "Jorge Ramírez", "Contado", "Herramientas diversas", "https://hf.com", "Ferretería", "2025-01-10", "activo"),
        ("Energía y Combustibles", "Energía EC S.A.", "NIT014", "Refinería 1111", "555-0014", "ec@example.com", "Diana Herrera", "15 días", "Combustibles y energía", "https://ec.com", "Energía", "2025-02-15", "activo"),
        ("Limpieza y Aseo", "Limpieza LA S.A.", "NIT015", "Calle Limpia 1212", "555-0015", "la@example.com", "Andrés Jiménez", "30 días", "Productos de limpieza", "https://la.com", "Limpieza", "2025-03-20", "activo"),
        ("Jardinería y Paisajismo", "Jardinería JP S.A.", "NIT016", "Vivero 1313", "555-0016", "jp@example.com", "Mónica Silva", "Contado", "Plantas y jardinería", "https://jp.com", "Jardinería", "2025-04-25", "activo"),
        ("Seguridad y Vigilancia", "Seguridad SV S.A.", "NIT017", "Av. Seguridad 1414", "555-0017", "sv@example.com", "Ricardo Mendoza", "30 días", "Servicios de seguridad", "https://sv.com", "Seguridad", "2025-05-30", "activo"),
        ("Mantenimiento y Reparación", "Mantenimiento MR S.A.", "NIT018", "Taller 1515", "555-0018", "mr@example.com", "Gloria Paredes", "15 días", "Servicios de mantenimiento", "https://mr.com", "Mantenimiento", "2025-06-05", "inactivo"),
        ("Publicidad y Marketing", "Publicidad PM S.A.", "NIT019", "Agencia 1616", "555-0019", "pm@example.com", "Héctor Vargas", "30 días", "Servicios publicitarios", "https://pm.com", "Publicidad", "2025-07-10", "activo"),
        ("Consultoría Empresarial", "Consultoría CE S.A.", "NIT020", "Oficina 1717", "555-0020", "ce@example.com", "Verónica Campos", "60 días", "Consultoría especializada", "https://ce.com", "Consultoría", "2025-08-15", "activo"),
    ]
    
    cursor = conn.cursor()
    for prov in proveedores:
        try:
            cursor.execute('''
                INSERT INTO proveedores 
                (nombre, razon_social, nit, direccion, telefono, email, contacto, condiciones_pago, notas, sitio_web, producto_servicio, fecha_registro, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', prov)
        except sqlite3.IntegrityError:
            print(f"  [ADVERTENCIA] Proveedor {prov[0]} ya existe (NIT duplicado), omitiendo...")
    
    conn.commit()
    print(f"  [OK] {len(proveedores)} proveedores insertados\n")


def seed_clientes(conn):
    """Inserta 20 clientes de prueba."""
    print("Insertando 20 clientes...")
    
    clientes = [
        ("Empresa Comercial SA", "persona_moral", "RFC001", "Calle Comercial 100", "555-1001", "comercial@example.com", "Gerente General", 50000.0, 1),
        ("Juan Pérez García", "persona_fisica", "RFC002", "Av. Residencial 200", "555-1002", "juan@example.com", "Juan Pérez", 10000.0, 1),
        ("Constructora Edificios", "persona_moral", "RFC003", "Zona Construcción 300", "555-1003", "constructora@example.com", "Ing. Director", 100000.0, 1),
        ("María López Sánchez", "persona_fisica", "RFC004", "Calle Privada 400", "555-1004", "maria@example.com", "María López", 5000.0, 1),
        ("Distribuidora Regional", "persona_moral", "RFC005", "Centro Distribución 500", "555-1005", "distrib@example.com", "Director Comercial", 75000.0, 1),
        ("Carlos Rodríguez", "persona_fisica", "RFC006", "Colonia Centro 600", "555-1006", "carlos@example.com", "Carlos Rodríguez", 15000.0, 1),
        ("Farmacia Central", "persona_moral", "RFC007", "Av. Salud 700", "555-1007", "farmacia@example.com", "Farmacéutico", 30000.0, 1),
        ("Ana Martínez Torres", "persona_fisica", "RFC008", "Residencial Norte 800", "555-1008", "ana@example.com", "Ana Martínez", 8000.0, 1),
        ("Supermercado Popular", "persona_moral", "RFC009", "Mall Comercial 900", "555-1009", "super@example.com", "Gerente Tienda", 120000.0, 1),
        ("Luis Sánchez Díaz", "persona_fisica", "RFC010", "Barrio Sur 1000", "555-1010", "luis@example.com", "Luis Sánchez", 12000.0, 1),
        ("Taller Mecánico Auto", "persona_moral", "RFC011", "Zona Industrial 1100", "555-1011", "taller@example.com", "Mecánico Jefe", 25000.0, 1),
        ("Patricia Gómez", "persona_fisica", "RFC012", "Calle Flores 1200", "555-1012", "patricia@example.com", "Patricia Gómez", 6000.0, 1),
        ("Restaurante El Buen Sabor", "persona_moral", "RFC013", "Av. Gastronómica 1300", "555-1013", "restaurante@example.com", "Chef Propietario", 40000.0, 1),
        ("Roberto Hernández", "persona_fisica", "RFC014", "Colonia Nueva 1400", "555-1014", "roberto@example.com", "Roberto Hernández", 9000.0, 1),
        ("Hotel Plaza Central", "persona_moral", "RFC015", "Centro Histórico 1500", "555-1015", "hotel@example.com", "Gerente Hotel", 150000.0, 1),
        ("Carmen Ruiz Vega", "persona_fisica", "RFC016", "Residencial Este 1600", "555-1016", "carmen@example.com", "Carmen Ruiz", 7000.0, 1),
        ("Clínica Médica", "persona_moral", "RFC017", "Av. Médica 1700", "555-1017", "clinica@example.com", "Director Médico", 80000.0, 1),
        ("Fernando Torres", "persona_fisica", "RFC018", "Barrio Oeste 1800", "555-1018", "fernando@example.com", "Fernando Torres", 11000.0, 1),
        ("Escuela Primaria", "persona_moral", "RFC019", "Zona Educativa 1900", "555-1019", "escuela@example.com", "Director Escolar", 20000.0, 1),
        ("Laura Vega Castro", "persona_fisica", "RFC020", "Calle Estudiantes 2000", "555-1020", "laura@example.com", "Laura Vega", 5000.0, 0),
    ]
    
    cursor = conn.cursor()
    for cli in clientes:
        try:
            cursor.execute('''
                INSERT INTO clientes 
                (nombre, tipo, rfc, direccion, telefono, email, contacto, credito_limite, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', cli)
        except sqlite3.IntegrityError:
            print(f"  [ADVERTENCIA] Cliente {cli[0]} ya existe, omitiendo...")
    
    conn.commit()
    print(f"  [OK] {len(clientes)} clientes insertados\n")


def seed_empleados(conn):
    """Inserta 20 empleados de prueba."""
    print("Insertando 20 empleados...")
    
    empleados = [
        ("Pedro", "García", "López", "CURP001", "Gerente General", "Dirección", "2020-01-15", 50000.0, "pedro@empresa.com", "555-2001", 1),
        ("María", "Rodríguez", "Sánchez", "CURP002", "Contador", "Contabilidad", "2020-02-20", 35000.0, "maria@empresa.com", "555-2002", 1),
        ("Juan", "Martínez", "Torres", "CURP003", "Vendedor", "Ventas", "2020-03-10", 25000.0, "juan@empresa.com", "555-2003", 1),
        ("Ana", "López", "Díaz", "CURP004", "Almacenista", "Almacén", "2020-04-05", 20000.0, "ana@empresa.com", "555-2004", 1),
        ("Carlos", "González", "Ruiz", "CURP005", "Supervisor", "Operaciones", "2020-05-12", 30000.0, "carlos@empresa.com", "555-2005", 1),
        ("Laura", "Hernández", "Vega", "CURP006", "Asistente", "Administración", "2020-06-18", 22000.0, "laura@empresa.com", "555-2006", 1),
        ("Roberto", "Pérez", "Castro", "CURP007", "Chofer", "Logística", "2020-07-22", 18000.0, "roberto@empresa.com", "555-2007", 1),
        ("Carmen", "Sánchez", "Morales", "CURP008", "Recepcionista", "Recepción", "2020-08-30", 20000.0, "carmen@empresa.com", "555-2008", 1),
        ("Fernando", "Torres", "Ramírez", "CURP009", "Técnico", "Mantenimiento", "2020-09-14", 28000.0, "fernando@empresa.com", "555-2009", 1),
        ("Patricia", "Díaz", "Jiménez", "CURP010", "Analista", "Sistemas", "2020-10-08", 32000.0, "patricia@empresa.com", "555-2010", 1),
        ("Miguel", "Ruiz", "Silva", "CURP011", "Vendedor", "Ventas", "2021-01-15", 25000.0, "miguel@empresa.com", "555-2011", 1),
        ("Sandra", "Vega", "Mendoza", "CURP012", "Contador", "Contabilidad", "2021-02-20", 35000.0, "sandra@empresa.com", "555-2012", 1),
        ("Jorge", "Castro", "Paredes", "CURP013", "Supervisor", "Almacén", "2021-03-10", 30000.0, "jorge@empresa.com", "555-2013", 1),
        ("Diana", "Morales", "Vargas", "CURP014", "Asistente", "Ventas", "2021-04-05", 22000.0, "diana@empresa.com", "555-2014", 1),
        ("Andrés", "Ramírez", "Campos", "CURP015", "Técnico", "IT", "2021-05-12", 38000.0, "andres@empresa.com", "555-2015", 1),
        ("Mónica", "Jiménez", "Herrera", "CURP016", "Gerente", "Ventas", "2021-06-18", 45000.0, "monica@empresa.com", "555-2016", 1),
        ("Ricardo", "Silva", "Gómez", "CURP017", "Chofer", "Logística", "2021-07-22", 18000.0, "ricardo@empresa.com", "555-2017", 1),
        ("Gloria", "Mendoza", "López", "CURP018", "Almacenista", "Almacén", "2021-08-30", 20000.0, "gloria@empresa.com", "555-2018", 1),
        ("Héctor", "Paredes", "Martínez", "CURP019", "Vendedor", "Ventas", "2021-09-14", 25000.0, "hector@empresa.com", "555-2019", 1),
        ("Verónica", "Vargas", "Rodríguez", "CURP020", "Asistente", "Dirección", "2021-10-08", 24000.0, "veronica@empresa.com", "555-2020", 0),
    ]
    
    cursor = conn.cursor()
    for emp in empleados:
        try:
            cursor.execute('''
                INSERT INTO empleados 
                (nombre, apellido_paterno, apellido_materno, identificacion, puesto, departamento, fecha_contratacion, salario, email, telefono, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', emp)
        except sqlite3.IntegrityError:
            print(f"  [ADVERTENCIA] Empleado {emp[0]} {emp[1]} ya existe, omitiendo...")
    
    conn.commit()
    print(f"  [OK] {len(empleados)} empleados insertados\n")


def seed_productos(conn):
    """Inserta 20 productos de prueba."""
    print("Insertando 20 productos...")
    
    productos = [
        ("SKU001", "Laptop Dell Inspiron", "Laptop 15 pulgadas, 8GB RAM, 256GB SSD", "Electrónica", "Unidad", 45000.0, 55000.0, 5.0, 1),
        ("SKU002", "Mouse Inalámbrico", "Mouse óptico inalámbrico USB", "Electrónica", "Unidad", 250.0, 350.0, 20.0, 1),
        ("SKU003", "Teclado Mecánico", "Teclado mecánico RGB", "Electrónica", "Unidad", 800.0, 1200.0, 15.0, 1),
        ("SKU004", "Monitor 24 pulgadas", "Monitor Full HD 1920x1080", "Electrónica", "Unidad", 3500.0, 4500.0, 10.0, 1),
        ("SKU005", "Impresora Multifuncional", "Impresora láser color", "Electrónica", "Unidad", 8500.0, 11000.0, 3.0, 1),
        ("SKU006", "Papel A4", "Resma de papel A4 500 hojas", "Oficina", "Resma", 120.0, 180.0, 50.0, 1),
        ("SKU007", "Lápices #2", "Caja de 12 lápices HB", "Oficina", "Caja", 25.0, 40.0, 100.0, 1),
        ("SKU008", "Marcadores Permanentes", "Set de 4 marcadores permanentes", "Oficina", "Set", 35.0, 55.0, 80.0, 1),
        ("SKU009", "Carpeta Archivadora", "Carpeta con gancho metálico", "Oficina", "Unidad", 45.0, 70.0, 60.0, 1),
        ("SKU010", "Calculadora Científica", "Calculadora científica con 240 funciones", "Oficina", "Unidad", 350.0, 500.0, 25.0, 1),
        ("SKU011", "Cemento Portland", "Bolsa de cemento 50 kg", "Construcción", "Bolsa", 280.0, 350.0, 200.0, 1),
        ("SKU012", "Ladrillo Rojo", "Ladrillo estándar 7x14x28 cm", "Construcción", "Pieza", 2.5, 3.5, 5000.0, 1),
        ("SKU013", "Varilla #3", "Varilla de acero corrugado 12m", "Construcción", "Pieza", 120.0, 160.0, 100.0, 1),
        ("SKU014", "Arena Fina", "Metro cúbico de arena fina", "Construcción", "m³", 450.0, 600.0, 50.0, 1),
        ("SKU015", "Pintura Blanca", "Galón de pintura blanca látex", "Construcción", "Galón", 180.0, 250.0, 40.0, 1),
        ("SKU016", "Aceite Motor 5W-30", "Aceite sintético 4 litros", "Automotriz", "Litro", 180.0, 250.0, 30.0, 1),
        ("SKU017", "Filtro de Aire", "Filtro de aire para automóvil", "Automotriz", "Unidad", 120.0, 180.0, 25.0, 1),
        ("SKU018", "Batería 12V 60Ah", "Batería de automóvil 12V", "Automotriz", "Unidad", 1200.0, 1600.0, 10.0, 1),
        ("SKU019", "Llanta 185/65R15", "Llanta radial 185/65R15", "Automotriz", "Unidad", 1200.0, 1600.0, 20.0, 1),
        ("SKU020", "Aceite Hidráulico", "Aceite hidráulico ISO 46, 20 litros", "Automotriz", "Litro", 85.0, 120.0, 15.0, 1),
    ]
    
    cursor = conn.cursor()
    for prod in productos:
        try:
            cursor.execute('''
                INSERT INTO productos 
                (sku, nombre, descripcion, categoria, unidad_medida, precio_costo, precio_venta, stock_minimo, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', prod)
        except sqlite3.IntegrityError:
            print(f"  [ADVERTENCIA] Producto {prod[0]} ya existe, omitiendo...")
    
    conn.commit()
    print(f"  [OK] {len(productos)} productos insertados\n")


def seed_compras(conn):
    """Inserta 20 compras de prueba."""
    print("Insertando 20 compras...")
    
    cursor = conn.cursor()
    
    # Obtener IDs de proveedores y empleados
    proveedores = cursor.execute("SELECT id FROM proveedores LIMIT 20").fetchall()
    empleados = cursor.execute("SELECT id FROM empleados LIMIT 20").fetchall()
    productos = cursor.execute("SELECT id FROM productos LIMIT 20").fetchall()
    
    if not proveedores or not empleados or not productos:
        print("  [ADVERTENCIA] No hay proveedores, empleados o productos suficientes. Creando compras basicas...")
        return
    
    estados = ['registrada', 'recibida', 'cancelada']
    metodos = ['Efectivo', 'Transferencia', 'Cheque', 'Tarjeta']
    
    for i in range(20):
        proveedor_id = proveedores[i % len(proveedores)][0]
        empleado_id = empleados[i % len(empleados)][0]
        fecha = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d')
        estado = estados[i % len(estados)]
        metodo = metodos[i % len(metodos)]
        
        subtotal = round(random.uniform(1000, 50000), 2)
        impuesto = round(subtotal * 0.16, 2)
        descuento = round(subtotal * random.uniform(0, 0.1), 2)
        total = round(subtotal + impuesto - descuento, 2)
        
        try:
            cursor.execute('''
                INSERT INTO compras 
                (proveedor_id, fecha, numero_factura, serie, subtotal, impuesto, descuento, total, metodo_pago, estado, empleado_id, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                proveedor_id,
                fecha,
                f"FAC-{2024 + i % 2}-{str(i+1).zfill(5)}",
                "A",
                subtotal,
                impuesto,
                descuento,
                total,
                metodo,
                estado,
                empleado_id,
                f"Compra de prueba #{i+1}"
            ))
            
            compra_id = cursor.lastrowid
            
            # Crear detalle de compra
            producto_id = productos[i % len(productos)][0]
            cantidad = random.uniform(1, 50)
            precio_unitario = round(random.uniform(50, 5000), 2)
            subtotal_det = round(cantidad * precio_unitario, 2)
            impuesto_det = round(subtotal_det * 0.16, 2)
            
            cursor.execute('''
                INSERT INTO compras_detalle 
                (compra_id, producto_id, cantidad, unidad_medida, precio_unitario, subtotal, impuesto, descuento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (compra_id, producto_id, cantidad, "Unidad", precio_unitario, subtotal_det, impuesto_det, 0))
            
        except Exception as e:
            print(f"  [ERROR] Error al crear compra {i+1}: {e}")
    
    conn.commit()
    print(f"  [OK] 20 compras insertadas\n")


def seed_ventas(conn):
    """Inserta 20 ventas de prueba."""
    print("Insertando 20 ventas...")
    
    cursor = conn.cursor()
    
    # Obtener IDs de clientes, empleados y productos
    clientes = cursor.execute("SELECT id FROM clientes LIMIT 20").fetchall()
    empleados = cursor.execute("SELECT id FROM empleados LIMIT 20").fetchall()
    productos = cursor.execute("SELECT id FROM productos LIMIT 20").fetchall()
    
    if not clientes or not empleados or not productos:
        print("  [ADVERTENCIA] No hay clientes, empleados o productos suficientes. Creando ventas basicas...")
        return
    
    estados = ['pendiente', 'completada', 'cancelada']
    metodos = ['Efectivo', 'Transferencia', 'Cheque', 'Tarjeta', 'Crédito']
    
    for i in range(20):
        cliente_id = clientes[i % len(clientes)][0] if clientes[i % len(clientes)][0] else None
        empleado_id = empleados[i % len(empleados)][0]
        fecha = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
        estado = estados[i % len(estados)]
        metodo = metodos[i % len(metodos)]
        
        subtotal = round(random.uniform(500, 30000), 2)
        impuesto = round(subtotal * 0.16, 2)
        descuento = round(subtotal * random.uniform(0, 0.15), 2)
        total = round(subtotal + impuesto - descuento, 2)
        
        try:
            cursor.execute('''
                INSERT INTO ventas 
                (cliente_id, fecha, numero_factura, serie, subtotal, impuesto, descuento, total, metodo_pago, estado, empleado_id, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cliente_id,
                fecha,
                f"VTA-{2024 + i % 2}-{str(i+1).zfill(5)}",
                "A",
                subtotal,
                impuesto,
                descuento,
                total,
                metodo,
                estado,
                empleado_id,
                f"Venta de prueba #{i+1}"
            ))
            
            venta_id = cursor.lastrowid
            
            # Crear detalle de venta
            producto_id = productos[i % len(productos)][0]
            cantidad = random.uniform(1, 20)
            precio_unitario = round(random.uniform(100, 3000), 2)
            subtotal_det = round(cantidad * precio_unitario, 2)
            impuesto_det = round(subtotal_det * 0.16, 2)
            
            cursor.execute('''
                INSERT INTO ventas_detalle 
                (venta_id, producto_id, cantidad, unidad_medida, precio_unitario, subtotal, impuesto, descuento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (venta_id, producto_id, cantidad, "Unidad", precio_unitario, subtotal_det, impuesto_det, 0))
            
        except Exception as e:
            print(f"  [ERROR] Error al crear venta {i+1}: {e}")
    
    conn.commit()
    print(f"  [OK] 20 ventas insertadas\n")


def seed_almacen(conn):
    """Inserta 20 movimientos de almacén de prueba."""
    print("Insertando 20 movimientos de almacén...")
    
    cursor = conn.cursor()
    
    productos = cursor.execute("SELECT id FROM productos LIMIT 20").fetchall()
    empleados = cursor.execute("SELECT id FROM empleados LIMIT 20").fetchall()
    
    if not productos or not empleados:
        print("  [ADVERTENCIA] No hay productos o empleados suficientes. Creando movimientos basicos...")
        return
    
    tipos = ['entrada', 'salida', 'ajuste']
    referencias = ['compra', 'venta', 'ajuste', 'inventario']
    
    for i in range(20):
        producto_id = productos[i % len(productos)][0]
        empleado_id = empleados[i % len(empleados)][0]
        tipo = tipos[i % len(tipos)]
        referencia = referencias[i % len(referencias)]
        cantidad = round(random.uniform(1, 100), 2)
        fecha = (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
        
        try:
            cursor.execute('''
                INSERT INTO almacen 
                (producto_id, tipo_movimiento, cantidad, unidad_medida, referencia, referencia_id, fecha, motivo, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                producto_id,
                tipo,
                cantidad,
                "Unidad",
                referencia,
                i + 1,
                fecha,
                f"Movimiento de prueba #{i+1} - {tipo}",
                empleado_id
            ))
        except Exception as e:
            print(f"  [ERROR] Error al crear movimiento {i+1}: {e}")
    
    conn.commit()
    print(f"  [OK] 20 movimientos de almacen insertados\n")


def main():
    """Función principal que ejecuta todos los seeds."""
    if not DB_PATH.exists():
        print(f"[ERROR] No se encontro la base de datos en {DB_PATH}")
        print("   Por favor, ejecuta primero create_database.py para crear la base de datos.")
        return
    
    print("=" * 60)
    print("  SCRIPT DE DATOS DE PRUEBA")
    print("=" * 60)
    print(f"Base de datos: {DB_PATH}\n")
    
    conn = get_db_connection()
    
    try:
        seed_proveedores(conn)
        seed_clientes(conn)
        seed_empleados(conn)
        seed_productos(conn)
        seed_compras(conn)
        seed_ventas(conn)
        seed_almacen(conn)
        
        print("=" * 60)
        print("  [OK] PROCESO COMPLETADO")
        print("=" * 60)
        print("\nSe han insertado 20 registros de prueba en cada módulo.")
        print("Puedes verificar los datos en la aplicación.\n")
        
    except Exception as e:
        print(f"\n[ERROR] Error durante la insercion: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()

