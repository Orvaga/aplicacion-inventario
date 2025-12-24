# Guía de Despliegue - Aplicación de Inventario

## 📋 Archivos Creados para Despliegue

✅ requirements.txt - Dependencias Python
✅ render.yaml - Configuración Render
✅ Procfile - Comando de inicio
✅ runtime.txt - Versión Python
✅ .gitignore - Archivos a ignorar
✅ README.md - Documentación actualizada

## 🚀 Pasos para Subir a GitHub

### 1. Inicializar Git (si no está inicializado)
```bash
cd d:\huilawed\aplicacion_app
git init
```

### 2. Agregar todos los archivos
```bash
git add .
```

### 3. Hacer commit inicial
```bash
git commit -m "Initial commit - Aplicación de inventario con diseño moderno"
```

### 4. Crear repositorio en GitHub
- Ve a: https://github.com/new
- Nombre: `aplicacion-inventario` (o el que prefieras)
- Descripción: "Sistema de gestión de inventario con Flask"
- Público o Privado (tu elección)
- NO marques: README, .gitignore, o licencia
- Click "Create repository"

### 5. Conectar repositorio local con GitHub
```bash
git remote add origin https://github.com/TU_USUARIO/aplicacion-inventario.git
git branch -M main
git push -u origin main
```

## 🌐 Pasos para Desplegar en Render

### 1. Crear cuenta en Render
- Ve a: https://render.com
- Regístrate con GitHub (recomendado)
- Autoriza el acceso a tus repositorios

### 2. Crear Web Service
1. Click en "New +" → "Web Service"
2. Selecciona tu repositorio `aplicacion-inventario`
3. Configura:
   - **Name:** aplicacion-inventario
   - **Region:** Oregon (US West) o el más cercano
   - **Branch:** main
   - **Root Directory:** (dejar vacío)
   - **Environment:** Python 3
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python backend/create_database.py
     ```
   - **Start Command:** 
     ```
     gunicorn -w 4 -b 0.0.0.0:$PORT backend.run:app
     ```
   - **Plan:** Free

4. Click "Create Web Service"

### 3. Esperar el despliegue
- El primer despliegue toma 5-10 minutos
- Verás los logs en tiempo real
- Cuando termine, verás "Live" en verde

### 4. Acceder a tu aplicación
- URL: `https://aplicacion-inventario.onrender.com`
- O el nombre que hayas elegido

## 🔄 Actualizar la Aplicación

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

Render detectará automáticamente los cambios y redesplegar la aplicación.

## ⚠️ Notas Importantes

1. **Base de datos:** SQLite se reinicia en cada despliegue en el plan Free
   - Para persistencia, considera usar PostgreSQL (Render ofrece plan free)
   
2. **Plan Free de Render:**
   - La app se "duerme" después de 15 minutos de inactividad
   - Primera carga después de dormir toma ~30 segundos
   - 750 horas gratis al mes

3. **Variables de entorno:**
   - Si necesitas agregar variables, ve a:
   - Dashboard → Tu servicio → Environment → Add Environment Variable

## 🔧 Solución de Problemas

### Error: "Failed to build"
- Verifica que requirements.txt esté en la raíz
- Revisa los logs de build en Render

### Error: "Application failed to start"
- Verifica el Start Command
- Revisa los logs de runtime en Render

### La app no carga
- Espera 30 segundos (puede estar "despertando")
- Revisa los logs en Render Dashboard

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Render Dashboard
2. Verifica que todos los archivos estén en GitHub
3. Consulta la documentación de Render: https://render.com/docs

---

¡Listo! Tu aplicación estará disponible en internet 🎉
