import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time



# Función para extraer números de una página de PubMed
def extract_numbers_from_pubmed(pmid):
    url = f"https://pubmed.ncbi.nlm.nih.gov/?format=pmid&linkname=pubmed_pubmed_citedin&from_uid={pmid}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text()
        numbers = re.findall(r'\d+', page_text)
        return [int(num) for num in numbers]
    else:
        print(f"No se pudo acceder a la página para PMID {pmid}. Estado:", response.status_code)
        return []

# https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += str(ele) + ", "
    str1 = str1[:-2]
 
    # return string
    return str1



file_path = './clinicaltrials_limpio.csv'
df= pd.read_csv(file_path)


df['CitedBy'] = ["" for _ in range(len(df))]


# Array con diferentes PMIDs
pmids = df['ReferencePMID'].dropna().to_numpy()

# Iterando sobre los PMIDs y extrayendo números
all_numbers = {}
for pmid in pmids:
    df.loc[df['ReferencePMID'] == pmid, 'CitedBy'] =  listToString(extract_numbers_from_pubmed(str(int(pmid))))
    time.sleep(3)


# Especifica el path del CSV
ruta_archivo = './clinicaltrials_citations.csv'
# Guardar el DataFrame como CSV
df.to_csv(ruta_archivo, index=False, header=True)
