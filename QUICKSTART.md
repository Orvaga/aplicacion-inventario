# 🚀 INICIO RÁPIDO - Despliegue en 5 Minutos

## Opción 1: Script Automático (Recomendado)

### Ejecutar en PowerShell:
```powershell
cd d:\huilawed\aplicacion_app
.\deploy-to-github.ps1
```

El script te guiará paso a paso.

---

## Opción 2: Manual

### 1️⃣ Subir a GitHub (2 minutos)

```bash
# Inicializar Git
git init
git add .
git commit -m "Initial commit"

# Crear repo en GitHub: https://github.com/new
# Luego conectar:
git remote add origin https://github.com/TU_USUARIO/aplicacion-inventario.git
git branch -M main
git push -u origin main
```

### 2️⃣ Desplegar en Render (3 minutos)

1. **Ir a:** https://render.com
2. **Registrarse** con GitHub
3. **New + → Web Service**
4. **Seleccionar** tu repositorio
5. **Configurar:**
   - Name: `aplicacion-inventario`
   - Build: `pip install -r requirements.txt && python backend/create_database.py`
   - Start: `gunicorn -w 4 -b 0.0.0.0:$PORT backend.run:app`
   - Plan: Free
6. **Click:** Create Web Service
7. **Esperar** 5-10 minutos

### 3️⃣ ¡Listo! 🎉

Tu app estará en: `https://aplicacion-inventario.onrender.com`

---

## 📁 Archivos Creados

✅ `requirements.txt` - Dependencias
✅ `render.yaml` - Config Render
✅ `Procfile` - Comando inicio
✅ `runtime.txt` - Python 3.11
✅ `DEPLOYMENT.md` - Guía detallada
✅ `deploy-to-github.ps1` - Script automático
✅ `.gitignore` - Archivos ignorados
✅ `README.md` - Documentación

---

## ⚡ Comandos Útiles

### Actualizar después de cambios:
```bash
git add .
git commit -m "Descripción cambios"
git push
```

### Ver logs en Render:
Dashboard → Tu servicio → Logs

### Reiniciar servicio:
Dashboard → Tu servicio → Manual Deploy → Deploy latest commit

---

## 🆘 Problemas Comunes

**App no carga:**
- Espera 30 seg (puede estar "despertando")
- Plan Free se duerme tras 15 min inactividad

**Error de build:**
- Verifica requirements.txt en raíz
- Revisa logs en Render

**Base de datos vacía:**
- SQLite se reinicia en cada deploy (plan Free)
- Considera PostgreSQL para persistencia

---

## 📚 Más Información

- **Guía detallada:** `DEPLOYMENT.md`
- **Documentación:** `README.md`
- **Render Docs:** https://render.com/docs
- **GitHub Docs:** https://docs.github.com

---

**¿Listo para empezar?** 
Ejecuta: `.\deploy-to-github.ps1` 🚀
