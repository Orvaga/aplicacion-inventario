# Script para eliminar backend como submódulo y agregarlo correctamente
# Ejecutar en PowerShell desde aplicacion_app

Write-Host "🔧 Eliminando backend como submódulo..." -ForegroundColor Cyan

# 1. Eliminar .git de backend
Write-Host "`n📌 Paso 1: Eliminando .git de backend..." -ForegroundColor Yellow
Remove-Item -Path "backend\.git" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend\.gitignore" -Force -ErrorAction SilentlyContinue
Write-Host "✅ .git eliminado de backend" -ForegroundColor Green

# 2. Agregar todos los archivos de backend
Write-Host "`n📌 Paso 2: Agregando archivos de backend..." -ForegroundColor Yellow
git add backend -f
git add -A
Write-Host "✅ Archivos agregados" -ForegroundColor Green

# 3. Hacer commit
Write-Host "`n📌 Paso 3: Creando commit..." -ForegroundColor Yellow
git commit -m "Fix: Agregar todos los archivos de backend al repositorio"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit creado" -ForegroundColor Green
} else {
    Write-Host "⚠️  No hay cambios para commit" -ForegroundColor Yellow
}

# 4. Subir a GitHub
Write-Host "`n📌 Paso 4: Subiendo a GitHub..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ ¡Archivos subidos exitosamente!" -ForegroundColor Green
    Write-Host "`n🎉 BACKEND AGREGADO CORRECTAMENTE" -ForegroundColor Green
    Write-Host "`n📋 Ahora puedes:" -ForegroundColor Cyan
    Write-Host "1. Ir a GitHub y verificar que backend/ esté completo" -ForegroundColor White
    Write-Host "2. Eliminar el repositorio 'huilawed' en GitHub" -ForegroundColor White
    Write-Host "3. Desplegar en Render usando 'aplicacion-inventario'" -ForegroundColor White
} else {
    Write-Host "`n❌ Error al subir" -ForegroundColor Red
}
