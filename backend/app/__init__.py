from flask import Flask
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=str((app.instance_path and '') or '')
    )

    # Configure path to existing database in backend folder
    from pathlib import Path
    base = Path(__file__).resolve().parents[1]
    app.config['DATABASE'] = str(base / 'database.db')

    # ensure instance folder exists
    try:
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    # init db
    db.init_app(app)

    # register blueprints
    from .main import bp as main_bp
    from .productos import bp as productos_bp
    from .proveedores import bp as proveedores_bp
    from .compras import bp as compras_bp
    from .ventas import bp as ventas_bp
    from .almacen import bp as almacen_bp
    from .clientes import bp as clientes_bp
    from .empleados import bp as empleados_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(proveedores_bp)
    app.register_blueprint(compras_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(almacen_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(empleados_bp)

    return app
