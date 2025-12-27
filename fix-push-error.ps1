# Script para resolver conflicto con repositorio remoto
# Ejecutar en PowerShell

Write-Host "🔧 Resolviendo conflicto con GitHub..." -ForegroundColor Cyan

# Opción 1: Pull con rebase (recomendado)
Write-Host "`n📌 Descargando cambios del repositorio remoto..." -ForegroundColor Yellow
git pull origin main --rebase

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Cambios integrados correctamente" -ForegroundColor Green
    
    Write-Host "`n📌 Subiendo cambios a GitHub..." -ForegroundColor Yellow
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ ¡Código subido exitosamente!" -ForegroundColor Green
        Write-Host "`n🎉 REPOSITORIO SINCRONIZADO Y LISTO" -ForegroundColor Green
        Write-Host "`n🌐 Ahora puedes desplegar en Render:" -ForegroundColor Cyan
        Write-Host "   https://render.com" -ForegroundColor White
    } else {
        Write-Host "`n❌ Error al subir. Intenta manualmente:" -ForegroundColor Red
        Write-Host "   git push origin main" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n⚠️  Hay conflictos. Resolviendo con fuerza..." -ForegroundColor Yellow
    Write-Host "`n¿Quieres SOBRESCRIBIR el repositorio remoto con tu código local?" -ForegroundColor Red
    Write-Host "ADVERTENCIA: Esto eliminará cualquier cambio en GitHub" -ForegroundColor Red
    $respuesta = Read-Host "Escribe 'SI' para continuar"
    
    if ($respuesta -eq "SI") {
        Write-Host "`n📌 Forzando push..." -ForegroundColor Yellow
        git push origin main --force
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n✅ ¡Código subido con éxito!" -ForegroundColor Green
            Write-Host "🎉 REPOSITORIO ACTUALIZADO" -ForegroundColor Green
        } else {
            Write-Host "`n❌ Error al forzar push" -ForegroundColor Red
        }
    } else {
        Write-Host "`n❌ Operación cancelada" -ForegroundColor Yellow
        Write-Host "Resuelve los conflictos manualmente" -ForegroundColor Yellow
    }
}
