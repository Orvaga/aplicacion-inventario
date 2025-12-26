# Script para corregir y preparar el repositorio para Render
# Ejecutar en PowerShell

Write-Host "🔧 Corrigiendo repositorio para despliegue..." -ForegroundColor Cyan

# 1. Corregir URL del repositorio
Write-Host "`n📌 Paso 1: Corrigiendo URL del repositorio..." -ForegroundColor Yellow
git remote set-url origin https://github.com/orvaga/aplicacion-inventario.git

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ URL corregida" -ForegroundColor Green
} else {
    Write-Host "❌ Error al corregir URL" -ForegroundColor Red
    exit 1
}

# 2. Verificar URL
Write-Host "`n📌 Paso 2: Verificando URL..." -ForegroundColor Yellow
git remote -v
Write-Host "✅ URL verificada" -ForegroundColor Green

# 3. Agregar cambios
Write-Host "`n📌 Paso 3: Agregando cambios..." -ForegroundColor Yellow
git add .
Write-Host "✅ Cambios agregados" -ForegroundColor Green

# 4. Hacer commit
Write-Host "`n📌 Paso 4: Creando commit..." -ForegroundColor Yellow
git commit -m "Preparar aplicación para despliegue en Render - Diseño moderno completo"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit creado" -ForegroundColor Green
} else {
    Write-Host "⚠️  No hay cambios para commit (puede ser normal)" -ForegroundColor Yellow
}

# 5. Subir a GitHub
Write-Host "`n📌 Paso 5: Subiendo a GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ ¡Código subido exitosamente!" -ForegroundColor Green
    Write-Host "`n🎉 REPOSITORIO LISTO PARA RENDER" -ForegroundColor Green
    Write-Host "`n📋 Próximos pasos:" -ForegroundColor Cyan
    Write-Host "1. Ve a: https://render.com" -ForegroundColor White
    Write-Host "2. New + → Web Service" -ForegroundColor White
    Write-Host "3. Selecciona: orvaga/aplicacion-inventario" -ForegroundColor White
    Write-Host "4. Build Command: pip install -r requirements.txt && python backend/create_database.py" -ForegroundColor White
    Write-Host "5. Start Command: gunicorn -w 4 -b 0.0.0.0:`$PORT backend.run:app" -ForegroundColor White
    Write-Host "6. Plan: Free" -ForegroundColor White
    Write-Host "7. Create Web Service" -ForegroundColor White
    Write-Host "`n🌐 Tu app estará en: https://aplicacion-inventario.onrender.com" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Error al subir a GitHub" -ForegroundColor Red
    Write-Host "Verifica tus credenciales y permisos" -ForegroundColor Yellow
    Write-Host "Puede que necesites autenticarte con GitHub" -ForegroundColor Yellow
}

Write-Host "`n📖 Lee ESTADO_DEPLOY.md para más información" -ForegroundColor Yellow
