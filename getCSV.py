import requests
import json
import math
import pandas as pd

# Obtener número de registros que tratan el cancer de mama

# Definir la URL base y los parámetros de la consulta
base_url = "https://clinicaltrials.gov/api/query/study_fields"
params = {
    "expr": "cancer+breast",
    "fields": "NCTId,Condition,BriefTitle",
    "fmt": "JSON",
    "min_rnk": 1
}

# Realizar la solicitud a la API
response = requests.get(base_url, params=params)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()

    # Obtener el número total de registros que coinciden con la búsqueda
    total_records = data['StudyFieldsResponse']['NStudiesFound']
    print(f"Número total de registros encontrados: {total_records}")
else:
    print("Error en la solicitud: Código de estado", response.status_code)

# URL para obtener la lista de campos disponibles
fields_url = "https://classic.clinicaltrials.gov/api/info/study_fields_list?fmt=JSON"
# Limitador de columnas por petición
column_limit = 10 
# Limitador de filas por petición
row_limit = 1000

# Realizar la solicitud a la API
response = requests.get(fields_url)

if response.status_code == 200:
    data = response.json()

    # Extraer la lista de campos
    fields = data['StudyFields']['Fields']
    field_lots = [fields[i:i + column_limit] for i in range(0, len(fields), column_limit)]




else:
    print("Error en la solicitud: Código de estado", response.status_code)

# Inicializar un DataFrame vacío para almacenar los datos
df = pd.DataFrame()

for index_field, field_lot in enumerate(field_lots):

  # Convertir el array de campos en un string, separando cada campo con una coma
  fields_string = ",".join(field_lot)
  # print(str(index_field/len(field_lots)*100) + "%")

  # Definir la URL base y los parámetros de la consulta
  base_url = "https://clinicaltrials.gov/api/query/study_fields"
   
  # Inicializar un DataFrame vacío para almacenar un bloque con el limite de peticiones
  df_blck = pd.DataFrame()
  # Iterar en bloques
  for start in range(1, total_records+1, row_limit):
    
    end = min(start + row_limit-1, total_records) 

    # Definir los parámetros de la consulta para esta iteración
    params = {
         "expr": "cancer+breast",
         "fields": fields_string,
         "fmt": "JSON",
         "min_rnk": start,
         "max_rnk": end
     }
    # Realizar la solicitud a la API
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

          
        # Procesar y almacenar los datos en un DataFrame
        for study in data['StudyFieldsResponse']['StudyFields']:
            record = {field: study[field][0] if study[field] else None for field in params['fields'].split(',')}
            df_blck = pd.concat([df_blck, pd.DataFrame([record])], ignore_index=True)
    else:
        print("Error en la solicitud: Código de estado", response.status_code)

    
  # Incluir bloque en el dataset
  df = pd.concat((df, df_blck), axis=1)

# Path del CSV
ruta_archivo = './clinicaltrials_dataframe.csv'  

# Guardar el DataFrame como CSV
df.to_csv(ruta_archivo, index=False, header=True)