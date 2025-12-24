import connect_Db #Conectarnos a la base de datos
import Function_Query #Iniciar la funcion a la que le enviamos las Query (Consultas)
from Function_Query import run_query #Desde el archivo de Function Query llamamos la funcion, asi evitamos tener que llamar la funcion como un objeto es decir Function_Query.run_query("select * from Table")
import pandas as pd 

run_query("SELECT * FROM language ;")

run_query("SELECT * FROM Film;")

run_query("SELECT * from customer;")