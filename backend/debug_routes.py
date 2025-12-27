"""
Script para debugguear errores en rutas
"""
import sys
sys.path.insert(0, 'd:\\huilawed\\aplicacion_app')

from backend import create_app

app = create_app()

# Crear contexto de aplicación
with app.app_context():
    # Intentar ejecutar una ruta de prueba
    with app.test_client() as client:
        print("\n=== Testeando endpoints ===\n")
        
        # Test 1: Dashboard (debería funcionar)
        print("1. GET /")
        resp = client.get('/')
        print(f"   Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"   Error: {resp.data.decode('utf-8')[:500]}")
        
        # Test 2: Productos index
        print("\n2. GET /productos/")
        resp = client.get('/productos/')
        print(f"   Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"   Error: {resp.data.decode('utf-8')[:500]}")
        
        print("\n=== Fin de pruebas ===\n")
