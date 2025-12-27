import importlib.util
from pathlib import Path

pkg_init = Path(__file__).parent / 'app' / '__init__.py'
spec = importlib.util.spec_from_file_location('backend_app', str(pkg_init))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
create_app = getattr(mod, 'create_app')
app = create_app()
print('APP OK', app.import_name)
