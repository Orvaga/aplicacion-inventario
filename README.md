# Mi App - Aplicación Web con Flask

Aplicación web para gestión de inventario (proveedores, productos, compras, ventas, almacén, clientes, empleados).

## Estructura del Proyecto

```
aplicacion_app/
├── venv/                    # Entorno virtual
├── backend/                 # Backend (Flask)
│   ├── app/
│   │   ├── __init__.py      # Factory create_app()
│   │   ├── db.py            # Helper SQLite
│   │   ├── main/            # Blueprint principal
│   │   ├── templates/       # HTML templates (Jinja2)
│   │   └── static/          # CSS, JS, imágenes
│   ├── database.db          # Base de datos SQLite
│   ├── database_schema.sql  # DDL de las tablas
│   ├── create_database.py   # Script para crear/actualizar DB
│   ├── run.py               # Servidor Flask
│   └── requirements.txt      # Dependencias Python
├── requirements.txt         # Dependencias para despliegue
├── render.yaml              # Configuración Render
├── Procfile                 # Configuración proceso
├── runtime.txt              # Versión Python
├── .gitignore
└── README.md                # Este archivo
```

## Setup Local (Primeros Pasos)

### 1. Crear entorno virtual (una sola vez)

```powershell
Set-Location d:\huilawed\aplicacion_app
python -m venv venv
```

### 2. Activar entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

*(Si te pide permiso, ejecuta PowerShell como administrador o cambia la política: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

## Desarrollo Local

### Crear/actualizar base de datos

```powershell
python .\backend\create_database.py
```

### Ejecutar servidor Flask

```powershell
$env:PYTHONPATH = 'd:\huilawed\aplicacion_app'
python .\backend\run.py
```

Luego abre tu navegador en: **http://127.0.0.1:5000/**

### Desactivar entorno virtual

```powershell
deactivate
```

## Despliegue en Render

### Paso 1: Subir a GitHub

1. **Inicializar repositorio Git:**
```bash
git init
git add .
git commit -m "Initial commit - Aplicación de inventario"
```

2. **Crear repositorio en GitHub:**
   - Ve a https://github.com/new
   - Crea un nuevo repositorio (p.ej. `aplicacion-inventario`)
   - NO inicialices con README, .gitignore o licencia

3. **Conectar y subir:**
```bash
git remote add origin https://github.com/TU_USUARIO/aplicacion-inventario.git
git branch -M main
git push -u origin main
```

### Paso 2: Desplegar en Render

1. **Crear cuenta en Render:**
   - Ve a https://render.com
   - Regístrate o inicia sesión
   - Conecta tu cuenta de GitHub

2. **Crear nuevo Web Service:**
   - Click en "New +" → "Web Service"
   - Selecciona tu repositorio `aplicacion-inventario`
   - Configura:
     - **Name:** `aplicacion-inventario`
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt && python backend/create_database.py`
     - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT backend.run:app`
     - **Plan:** Free

3. **Desplegar:**
   - Click en "Create Web Service"
   - Espera a que termine el despliegue (5-10 minutos)
   - Tu app estará disponible en: `https://aplicacion-inventario.onrender.com`

### Actualizaciones Automáticas

Cada vez que hagas `git push` a GitHub, Render desplegará automáticamente los cambios.

```bash
git add .
git commit -m "Descripción de cambios"
git push
```

## Tablas de la Base de Datos

- **proveedores** — Información de proveedores
- **clientes** — Datos de clientes
- **empleados** — Personal
- **productos** — Catálogo de productos (SKU, nombre, precio, etc.)
- **compras** — Compras a proveedores (cabecera + detalle)
- **ventas** — Ventas a clientes (cabecera + detalle)
- **almacen** — Movimientos de inventario (entradas, salidas, ajustes)
- **stock** — Stock por ubicación (opcional)

## Características

✅ CRUD completo para todos los módulos
✅ Diseño moderno y responsivo
✅ Formularios compactos sin scroll
✅ Paginación y búsqueda
✅ Confirmación de eliminación con advertencias
✅ Base de datos SQLite

## Tecnologías

- **Backend:** Flask (Python)
- **Base de datos:** SQLite
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Despliegue:** Render
- **Servidor:** Gunicorn

## Notas

- La base de datos usa **SQLite** (archivo `database.db` en `backend/`)
- El servidor corre en **modo producción** con Gunicorn
- Las dependencias están listadas en `requirements.txt`
- **IMPORTANTE:** Nunca subas API keys o credenciales a GitHub

---

**Última actualización:** Enero 2025
