"""Script simple para crear `database.db` usando `database_schema.sql`.

Uso (PowerShell):
  python .\create_database.py

El script lee `database_schema.sql` en la misma carpeta y ejecuta todo el DDL.
"""
import sqlite3
from pathlib import Path
import sys


BASE = Path(__file__).parent
DB_PATH = BASE / "database.db"
SQL_PATH = BASE / "database_schema.sql"


def main():
    if not SQL_PATH.exists():
        print(f"No se encontró {SQL_PATH}. Asegúrate de estar en la carpeta correcta.")
        sys.exit(1)

    sql = SQL_PATH.read_text(encoding="utf-8")

    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.executescript(sql)
        conn.commit()
        print(f"Base de datos creada/actualizada en: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
