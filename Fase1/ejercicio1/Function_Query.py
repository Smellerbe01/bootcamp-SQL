# librerías
import connect_Db 
from connect_Db import connect_db
import pandas as pd

def run_query(query):
    conn = connect_db()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        cur.execute(query)
        df = cur.fetchall()
        dataframe = pd.DataFrame(df, columns=[desc[0] for desc in cur.description])
        print (dataframe)
        return dataframe
    except Exception as e:
        print("Error al ejecutar la consulta", e)
        return None
    finally:
        cur.close()
        conn.close()
