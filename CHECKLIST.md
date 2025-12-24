# ✅ CHECKLIST DE DESPLIEGUE

## Antes de Empezar

- [ ] Git instalado (verifica con: `git --version`)
- [ ] Cuenta de GitHub creada (https://github.com)
- [ ] Cuenta de Render creada (https://render.com)

---

## Paso 1: Preparar Proyecto ✅ COMPLETADO

- [✅] requirements.txt creado
- [✅] render.yaml creado
- [✅] Procfile creado
- [✅] runtime.txt creado
- [✅] .gitignore actualizado
- [✅] README.md actualizado
- [✅] Documentación creada

---

## Paso 2: Subir a GitHub

### Opción A: Script Automático
- [ ] Abrir PowerShell en `d:\huilawed\aplicacion_app`
- [ ] Ejecutar: `.\deploy-to-github.ps1`
- [ ] Seguir las instrucciones del script
- [ ] Crear repositorio en GitHub cuando se solicite
- [ ] Ingresar URL del repositorio

### Opción B: Manual
- [ ] Abrir terminal en `d:\huilawed\aplicacion_app`
- [ ] Ejecutar: `git init`
- [ ] Ejecutar: `git add .`
- [ ] Ejecutar: `git commit -m "Initial commit"`
- [ ] Crear repositorio en GitHub: https://github.com/new
- [ ] Ejecutar: `git remote add origin URL_DEL_REPO`
- [ ] Ejecutar: `git branch -M main`
- [ ] Ejecutar: `git push -u origin main`

---

## Paso 3: Desplegar en Render

- [ ] Ir a: https://render.com
- [ ] Iniciar sesión / Registrarse
- [ ] Conectar cuenta de GitHub
- [ ] Click en "New +" → "Web Service"
- [ ] Seleccionar repositorio: `aplicacion-inventario`
- [ ] Configurar:
  - [ ] Name: `aplicacion-inventario`
  - [ ] Environment: `Python 3`
  - [ ] Build Command: `pip install -r requirements.txt && python backend/create_database.py`
  - [ ] Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT backend.run:app`
  - [ ] Plan: `Free`
- [ ] Click "Create Web Service"
- [ ] Esperar 5-10 minutos

---

## Paso 4: Verificar Despliegue

- [ ] Ver logs en Render Dashboard
- [ ] Esperar mensaje "Live" en verde
- [ ] Copiar URL de la aplicación
- [ ] Abrir URL en navegador
- [ ] Verificar que la app carga correctamente
- [ ] Probar crear un proveedor
- [ ] Probar crear un producto
- [ ] Verificar navegación entre módulos

---

## Paso 5: Configuración Adicional (Opcional)

- [ ] Configurar dominio personalizado (si tienes uno)
- [ ] Configurar variables de entorno (si necesitas)
- [ ] Configurar PostgreSQL (para persistencia)
- [ ] Configurar notificaciones de deploy
- [ ] Configurar auto-deploy desde GitHub

---

## Solución de Problemas

### Si el build falla:
- [ ] Verificar que requirements.txt esté en la raíz
- [ ] Revisar logs de build en Render
- [ ] Verificar sintaxis de render.yaml

### Si la app no inicia:
- [ ] Verificar Start Command
- [ ] Revisar logs de runtime en Render
- [ ] Verificar que run.py esté correcto

### Si la app no carga:
- [ ] Esperar 30 segundos (puede estar despertando)
- [ ] Verificar URL correcta
- [ ] Revisar logs en Render Dashboard

---

## Actualizaciones Futuras

Cada vez que hagas cambios:

- [ ] Hacer cambios en el código
- [ ] Ejecutar: `git add .`
- [ ] Ejecutar: `git commit -m "Descripción"`
- [ ] Ejecutar: `git push`
- [ ] Esperar auto-deploy en Render (2-5 min)
- [ ] Verificar cambios en la URL

---

## URLs Importantes

📌 **Tu Repositorio GitHub:**
   https://github.com/TU_USUARIO/aplicacion-inventario

📌 **Tu App en Render:**
   https://aplicacion-inventario.onrender.com

📌 **Dashboard Render:**
   https://dashboard.render.com

📌 **Documentación:**
   - QUICKSTART.md (inicio rápido)
   - DEPLOYMENT.md (guía detallada)
   - README.md (documentación completa)

---

## ¡Listo! 🎉

Una vez completados todos los pasos, tu aplicación estará:
✅ En GitHub (código fuente)
✅ En Render (aplicación en vivo)
✅ Accesible desde cualquier lugar
✅ Con auto-deploy configurado

---

**Fecha de despliegue:** _________________

**URL de la aplicación:** _________________

**Notas adicionales:**
_________________________________________________
_________________________________________________
_________________________________________________
