# librerías

import psycopg2

# conexión a la base de datos

# 1. Conexión a la base de datos PostgreSQL

def connect_db( ):
    try:
        conn = psycopg2.connect( # se conecta a la base de datos
            host="localhost",
            database= "pagila", # nombre de la base de datos
            user="postgres", # usuario Conectado
            password="123456789",   
            port="5432"
        )
        print("Conexión exitosa")
        return conn # retorna la conexión
    except Exception as e: # manejo de errores
        print("Error de conexión", e)
        return None

