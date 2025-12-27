"""
Script de pruebas de humo (smoke tests) para validar endpoints principales.
Ejecutar contra servidor en background: python test_smoke.py
"""

import requests
import sys
import time

BASE_URL = "http://localhost:5000"

# Colores para output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def test_endpoint(method, endpoint, data=None, expect_code=200, description=""):
    """Prueba un endpoint y reporta resultado."""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            resp = requests.get(url, timeout=5)
        elif method == "POST":
            resp = requests.post(url, data=data, timeout=5)
        else:
            return False, f"Método {method} no soportado"
        
        if resp.status_code == expect_code:
            print(f"{GREEN}✓{RESET} {method:4s} {endpoint:30s} {description}")
            return True, resp.status_code
        else:
            print(f"{RED}✗{RESET} {method:4s} {endpoint:30s} Expected {expect_code}, got {resp.status_code}")
            return False, resp.status_code
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗{RESET} {method:4s} {endpoint:30s} Connection error (servidor no disponible)")
        return False, None
    except Exception as e:
        print(f"{RED}✗{RESET} {method:4s} {endpoint:30s} Error: {str(e)}")
        return False, None


def run_smoke_tests():
    """Ejecuta suite de pruebas de humo."""
    print("\n" + "=" * 80)
    print(f"  PRUEBAS DE HUMO - BASE_URL: {BASE_URL}")
    print("=" * 80 + "\n")
    
    passed = 0
    failed = 0
    
    # Esperar a que el servidor esté listo
    print(f"{YELLOW}Esperando servidor...{RESET}\n")
    for i in range(10):
        try:
            resp = requests.get(f"{BASE_URL}/", timeout=2)
            break
        except:
            if i < 9:
                time.sleep(1)
            else:
                print(f"{RED}Servidor no disponible después de 10 segundos{RESET}")
                return False
    
    # Pruebas de endpoints principales
    tests = [
        ("GET", "/", None, 200, "Dashboard principal"),
        
        # Productos
        ("GET", "/productos/", None, 200, "Listar productos"),
        ("GET", "/productos/create", None, 200, "Formulario crear producto"),
        
        # Proveedores
        ("GET", "/proveedores/", None, 200, "Listar proveedores"),
        ("GET", "/proveedores/create", None, 200, "Formulario crear proveedor"),
        
        # Clientes
        ("GET", "/clientes/", None, 200, "Listar clientes"),
        ("GET", "/clientes/create", None, 200, "Formulario crear cliente"),
        
        # Empleados
        ("GET", "/empleados/", None, 200, "Listar empleados"),
        ("GET", "/empleados/create", None, 200, "Formulario crear empleado"),
        
        # Compras
        ("GET", "/compras/", None, 200, "Listar compras"),
        ("GET", "/compras/create", None, 200, "Formulario crear compra"),
        
        # Ventas
        ("GET", "/ventas/", None, 200, "Listar ventas"),
        ("GET", "/ventas/create", None, 200, "Formulario crear venta"),
        
        # Almacén
        ("GET", "/almacen/", None, 200, "Listar movimientos almacén"),
        ("GET", "/almacen/registrar", None, 200, "Formulario registrar movimiento"),
    ]
    
    print(f"{'Método':<6} {'Endpoint':<32} {'Descripción':<30}\n")
    
    for method, endpoint, data, expect_code, description in tests:
        success, code = test_endpoint(method, endpoint, data, expect_code, description)
        if success:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"RESULTADOS: {GREEN}{passed} pasadas{RESET}, {RED}{failed} falló{RESET}")
    print("=" * 80 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1)
