from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, cast
from mysql.connector.cursor import MySQLCursorDict  # opción C si la prefieres

# Carga .env desde la raíz
load_dotenv(find_dotenv())

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),        # <— corregidos nombres
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "residentes_db"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )

def fetch_all_residentes() -> List[Dict[str, Any]]:
    """
    Ejecuta SELECT * FROM residentes y devuelve una lista de dicts.
    """
    conn = None
    try:
        conn = get_connection()
        # Opción C (anotación explícita del cursor):
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute(
                "SELECT * FROM residentes;"
            )
            # Opción A: cast para contentar al type checker
            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows

            # Opción B alternativa (sin cast):
            # return [dict(row) for row in cur.fetchall()]
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()