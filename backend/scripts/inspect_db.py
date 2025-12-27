import sqlite3
from pathlib import Path
p = Path(__file__).parent.parent / 'database.db'
print('DB path:', p, 'exists:', p.exists())
if not p.exists():
    print('DB does not exist')
else:
    conn = sqlite3.connect(str(p))
    for tbl in ('clientes','proveedores'):
        print('\nTable:', tbl)
        cur = conn.execute(f"PRAGMA table_info({tbl});")
        rows = cur.fetchall()
        if len(rows) == 0:
            print('  (table missing or empty)')
        for r in rows:
            print('  ', r)
    conn.close()
