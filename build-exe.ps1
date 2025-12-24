# build-exe.ps1
# Script para empaquetar la aplicación con PyInstaller en Windows (PowerShell)
# Uso: ejecutar desde la raíz del proycd..becto:  `.uild-exe.ps1`

# 1) Activar venv si lo usas (opcional). Si quieres que el script cree/active el venv, descomenta líneas.
# python -m venv .venv
# .\.venv\Scripts\Activate.ps1

# 2) Instalar PyInstaller (si no está instalado)
pip install pyinstaller

# 3) Ejecutar PyInstaller.
#    Aquí usamos `--onefile` para generar un único EXE portable. Con `--onefile` PyInstaller
#    empaqueta todo en un único ejecutable autoextraíble, pero la primera ejecución será
#    algo más lenta y el EXE será más grande.
#
#    Notas sobre --add-data en Windows: el formato es "source;dest" (ruta relativa o absoluta).
#    Con --onefile los datos se extraen en tiempo de ejecución a un directorio temporal,
#    por lo que Flask debe poder localizar las plantillas y estáticos (PyInstaller gestiona esto
#    cuando se incluyen correctamente).
#
#    Añadimos también algunos `--hidden-import` comunes que PyInstaller a veces no detecta
#    automáticamente (p. ej. extensiones de Jinja2/Markupsafe).

pyinstaller --noconfirm --clean --onefile \
	--name aplicacion_app \
	--add-data "backend/app/templates;backend/app/templates" \
	--add-data "backend/app/static;backend/app/static" \
	--add-data "backend/database.db;backend/database.db" \
	--hidden-import jinja2.ext \
	--hidden-import markupsafe \
	--hidden-import packaging \
	backend/run.py

Write-Host "Build finalizado. Revisa la carpeta 'dist' para el ejecutable 'aplicacion_app.exe'."

# Opcional: si quieres un EXE sin consola (modo background) añade `--noconsole` a la línea de pyinstaller.
# Ten en cuenta que sin consola será más difícil ver errores durante pruebas.

