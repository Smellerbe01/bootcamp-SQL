# Función para listar todas las tablas en la base de datos
# y describir la estructura de una tabla específica

import connect_Db
from connect_Db import connect_db # show_schema.py
import pandas as pd
def list_tables(conn):
    cur = conn.cursor()
    cur.execute("""
      SELECT table_schema, table_name
      FROM information_schema.tables
      WHERE table_type='BASE TABLE'
        AND table_schema NOT IN ('pg_catalog','information_schema')
      ORDER BY table_schema, table_name;
    """)
    for schema, table in cur.fetchall():
        print(f"{schema}.{table}")
    cur.close()

def describe_table(conn, schema, table):
    cur = conn.cursor()
    print(f"\n=== {schema}.{table} ===")

    # columnas
    cur.execute("""
      SELECT column_name, data_type, is_nullable, column_default
      FROM information_schema.columns
      WHERE table_schema=%s AND table_name=%s
      ORDER BY ordinal_position;
    """, (schema, table))
    print("Columns:")
    for col in cur.fetchall():
        print("  ", col)

    # clave primaria
    cur.execute("""
      SELECT kcu.column_name
      FROM information_schema.table_constraints tc
      JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
      WHERE tc.constraint_type='PRIMARY KEY' AND tc.table_schema=%s AND tc.table_name=%s;
    """, (schema, table))
    print("Primary key:", [r[0] for r in cur.fetchall()])

    # claves foráneas
    cur.execute("""
      SELECT
        tc.constraint_name, kcu.column_name,
        ccu.table_schema AS foreign_table_schema, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name
      FROM information_schema.table_constraints tc
      JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
      JOIN information_schema.constraint_column_usage ccu
        ON ccu.constraint_name = tc.constraint_name
      WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema=%s AND tc.table_name=%s;
    """, (schema, table))
    for fk in cur.fetchall():
        print("  FK:", fk)

    # índices
    cur.execute("SELECT indexname, indexdef FROM pg_indexes WHERE schemaname=%s AND tablename=%s;", (schema, table))
    print("Indexes:")
    for idx in cur.fetchall():
        print("  ", idx)

    cur.close()

def solicit_table_info(table = None):
    table = input("Enter table name: ")
    return  table

def main(table = None):
    conn = connect_db()
    if not conn:
        return
    try:
        list_tables(conn)
        # Describir una tabla específica (ejemplo)
        describe_table(conn, "public", solicit_table_info(table)) # Solicitar tabla al usuario
    finally:
        conn.close()

if __name__ == "__main__":
    main()

