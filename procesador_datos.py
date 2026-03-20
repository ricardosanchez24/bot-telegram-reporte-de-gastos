import numpy as np
import pandas as pd
import json
from clasificacionDatos import clasificacion_datos

def procesador(data):
    #procesar tabla csv
    
    prueba = pd.read_csv(data)

    #convertir csv a DataFrame
    tabla = pd.DataFrame(prueba)

    #crear nueva columna con valores vacios
    tabla['categoria'] = ''

    #print(tabla.loc[0])
    #print(tabla)
    #convirtiendo toda la columna de descripcion en una lista
    lista_descripcion = tabla['descripcion'].tolist()

    # se pasa la lista al clasificador y se limpian los datos de respuesta
    lista_clasificacion = clasificacion_datos(lista_descripcion=lista_descripcion)
    lista_limpia = lista_clasificacion.replace("```json","")
    lista = json.loads(lista_limpia) #loasd convierte un strin json en una lista o diccionario

    #print(lista)
    #print(lista_clasificacion)

    # pegamos todas las categorias en su columna
    tabla['categoria'] = lista

    #print(tabla.index)

    resumen = tabla.groupby('categoria')['monto'].sum()

    tabla_resumen = resumen.reset_index()

    datos_procesados = (tabla_resumen['monto'].astype(str) + ' ' +'Bs' + ' ' + tabla_resumen['categoria']).tolist()

    return datos_procesados



#print(procesador('datos_prueba.csv'))