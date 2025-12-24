# Script para subir el proyecto a GitHub
# Ejecutar en PowerShell desde la raíz del proyecto

Write-Host "🚀 Iniciando proceso de subida a GitHub..." -ForegroundColor Green

# 1. Verificar si Git está instalado
Write-Host "`n📋 Verificando Git..." -ForegroundColor Yellow
$gitVersion = git --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git no está instalado. Descárgalo de: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green

# 2. Inicializar repositorio (si no existe)
Write-Host "`n📋 Inicializando repositorio Git..." -ForegroundColor Yellow
if (!(Test-Path ".git")) {
    git init
    Write-Host "✅ Repositorio Git inicializado" -ForegroundColor Green
} else {
    Write-Host "✅ Repositorio Git ya existe" -ForegroundColor Green
}

# 3. Agregar archivos
Write-Host "`n📋 Agregando archivos..." -ForegroundColor Yellow
git add .
Write-Host "✅ Archivos agregados" -ForegroundColor Green

# 4. Hacer commit
Write-Host "`n📋 Creando commit..." -ForegroundColor Yellow
git commit -m "Initial commit - Aplicación de inventario con diseño moderno"
Write-Host "✅ Commit creado" -ForegroundColor Green

# 5. Solicitar URL del repositorio
Write-Host "`n📋 Configuración de GitHub" -ForegroundColor Yellow
Write-Host "Por favor, crea un repositorio en GitHub:" -ForegroundColor Cyan
Write-Host "1. Ve a: https://github.com/new" -ForegroundColor Cyan
Write-Host "2. Nombre: aplicacion-inventario" -ForegroundColor Cyan
Write-Host "3. NO marques README, .gitignore, o licencia" -ForegroundColor Cyan
Write-Host "4. Click 'Create repository'" -ForegroundColor Cyan
Write-Host ""

$repoUrl = Read-Host "Ingresa la URL del repositorio (ej: https://github.com/usuario/aplicacion-inventario.git)"

if ($repoUrl -eq "") {
    Write-Host "❌ URL no proporcionada. Saliendo..." -ForegroundColor Red
    exit 1
}

# 6. Agregar remote
Write-Host "`n📋 Conectando con GitHub..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin $repoUrl
Write-Host "✅ Repositorio remoto configurado" -ForegroundColor Green

# 7. Cambiar a rama main
Write-Host "`n📋 Configurando rama principal..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ Rama 'main' configurada" -ForegroundColor Green

# 8. Push a GitHub
Write-Host "`n📋 Subiendo código a GitHub..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ ¡Código subido exitosamente a GitHub!" -ForegroundColor Green
    Write-Host "`n🌐 Próximos pasos:" -ForegroundColor Cyan
    Write-Host "1. Ve a: https://render.com" -ForegroundColor White
    Write-Host "2. Crea una cuenta y conecta con GitHub" -ForegroundColor White
    Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor White
    Write-Host "4. Selecciona tu repositorio" -ForegroundColor White
    Write-Host "5. Usa la configuración del archivo DEPLOYMENT.md" -ForegroundColor White
    Write-Host "`n📖 Lee DEPLOYMENT.md para instrucciones detalladas" -ForegroundColor Yellow
} else {
    Write-Host "`n❌ Error al subir a GitHub" -ForegroundColor Red
    Write-Host "Verifica tus credenciales y permisos" -ForegroundColor Yellow
}
