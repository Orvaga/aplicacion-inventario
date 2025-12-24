-- Esquema SQLite sugerido para `database.db`
PRAGMA foreign_keys = ON;

-- Tabla de proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    razon_social TEXT,
    nit TEXT UNIQUE,
    rfc TEXT,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    contacto TEXT,
    condiciones_pago TEXT,
    notas TEXT,
    sitio_web TEXT,
    producto_servicio TEXT,
    fecha_registro TEXT DEFAULT (datetime('now')),
    estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo','inactivo')),
    created_at TEXT DEFAULT (datetime('now')),
    activo INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT
);

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT DEFAULT 'persona_fisica', -- persona_fisica / persona_moral
    rfc TEXT,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    contacto TEXT,
    credito_limite REAL DEFAULT 0,
    activo INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT
);

-- Tabla de empleados
CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido_paterno TEXT,
    apellido_materno TEXT,
    identificacion TEXT, -- CURP, DNI, etc.
    puesto TEXT,
    departamento TEXT,
    fecha_contratacion TEXT,
    salario REAL,
    email TEXT,
    telefono TEXT,
    activo INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    unidad_medida TEXT,
    precio_costo REAL DEFAULT 0,
    precio_venta REAL DEFAULT 0,
    stock_minimo REAL DEFAULT 0,
    activo INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT
);

-- Tabla de compras (cabecera)
    updated_at TEXT
    proveedor_id INTEGER NOT NULL,
    fecha TEXT DEFAULT (datetime('now')),
    numero_factura TEXT,
    serie TEXT,
    subtotal REAL DEFAULT 0,
    impuesto REAL DEFAULT 0,
    descuento REAL DEFAULT 0,
    total REAL DEFAULT 0,
    metodo_pago TEXT,
    estado TEXT DEFAULT 'registrada', -- registrada / recibida / cancelada
    empleado_id INTEGER,
    notas TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
);

-- Detalle de compras (líneas)
CREATE TABLE IF NOT EXISTS compras_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compra_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad REAL NOT NULL,
    unidad_medida TEXT,
    precio_unitario REAL DEFAULT 0,
    subtotal REAL DEFAULT 0,
    impuesto REAL DEFAULT 0,
    descuento REAL DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla de ventas (cabecera)
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    fecha TEXT DEFAULT (datetime('now')),
    numero_factura TEXT,
    serie TEXT,
    subtotal REAL DEFAULT 0,
    impuesto REAL DEFAULT 0,
    descuento REAL DEFAULT 0,
    total REAL DEFAULT 0,
    activo INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT
    empleado_id INTEGER,
    notas TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
);

-- Detalle de ventas (líneas)
CREATE TABLE IF NOT EXISTS ventas_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad REAL NOT NULL,
    unidad_medida TEXT,
    precio_unitario REAL DEFAULT 0,
    subtotal REAL DEFAULT 0,
    impuesto REAL DEFAULT 0,
    descuento REAL DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla de movimientos de almacén (entradas/salidas/ajustes)
CREATE TABLE IF NOT EXISTS almacen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    tipo_movimiento TEXT NOT NULL, -- entrada / salida / ajuste
    cantidad REAL NOT NULL,
    unidad_medida TEXT,
    referencia TEXT, -- e.g., 'compra', 'venta', 'ajuste'
    referencia_id INTEGER,
    fecha TEXT DEFAULT (datetime('now')),
    motivo TEXT,
    usuario_id INTEGER,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (usuario_id) REFERENCES empleados(id)
);

-- Tabla opcional de stock por ubicación
CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    ubicacion TEXT,
    cantidad REAL NOT NULL DEFAULT 0,
    ultimo_movimiento TEXT,
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Índices recomendados
CREATE INDEX IF NOT EXISTS idx_productos_sku ON productos(sku);
CREATE INDEX IF NOT EXISTS idx_compras_proveedor ON compras(proveedor_id);
CREATE INDEX IF NOT EXISTS idx_ventas_cliente ON ventas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_almacen_producto ON almacen(producto_id);
CREATE INDEX IF NOT EXISTS idx_proveedores_nit ON proveedores(nit);
CREATE INDEX IF NOT EXISTS idx_proveedores_estado ON proveedores(estado);
