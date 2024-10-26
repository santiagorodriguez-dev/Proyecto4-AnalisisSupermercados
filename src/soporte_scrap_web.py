# Importamos las librerías que necesitamos

# Librerías de extracción de actividades
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore

# Tratamiento de actividades
# -----------------------------------------------------------------------
import pandas as pd # type: ignore
import numpy as np # type: ignore
import re
from time import sleep
import time
import multiprocessing
import asyncio
from datetime import datetime

# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver  # type: ignore # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # type: ignore # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # type: ignore # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import NoSuchElementException # type: ignore # Excepciones comunes de selenium que nos podemos encontrar
from selenium.webdriver.common.by import By # type: ignore


supermercados_dicc = {'mercadona': 1, 'carrefour': 2, 'eroski': 3, 'dia': 4, 'hipercor':5, 'alcampo':6}
categorias_dicc = {'aceite de girasol': 1, 'aceite de oliva': 2, 'leche': 3}

def get_urls(input_data):
    driver = webdriver.Chrome()
    urls_return = []
    url=input_data[0]
    driver.get(url)
    driver.maximize_window()
    sleep(5)
    driver.find_element('css selector','#rcc-confirm-button').click()
    sleep(5)
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, input_data[1])

    for i in links:
        urls_return.append(i.get_attribute("href"))

    driver.close()

    return urls_return

def procesar(input_data, texto): 

    retun_list = []
    
    args = [(i, texto) for i in input_data]

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        resultados = pool.map(get_urls, args)

    for res in resultados:
        retun_list.append(res)
   
    return retun_list

def get_list_productos(url_first):

    start_time = time.time()

    lista_all_productos = []

    list_urls_super = procesar(url_first,"Acceder")

    list_con_categorias=[]

    for supermecados in list_urls_super:
        list_con_categorias.append(procesar(supermecados,'Ver'))

    for k in list_con_categorias:
        for h in k:
            lista_all_productos.append(procesar(h,'Histórico'))

    
    end_time = time.time()
    print(f"\n Total scrapeo de urls duró {end_time - start_time:.2f} segundos.")

    return lista_all_productos

async def get_historico(url):

    df_historico_producto = pd.DataFrame()
   
    url_sopa = url

    res = requests.get(url_sopa)
    sopa = BeautifulSoup(res.content, "html.parser")

    resultado = sopa.find("tbody")
    result_tr = resultado.findAll("tr")
    
    if (res.status_code == 200 and resultado and result_tr):
        datos = url.split("/")[3:6]
        supermercado = ''
        categoria = ''
        desc_producto = datos[2]

        for x, y in supermercados_dicc.items():
            if (str(datos[0]).replace('-',' ') == x):
                supermercado = y
        
        for x, y in categorias_dicc.items():
            if (str(datos[1]).replace('-',' ') == x):
                categoria = y

        lista_historico = []
        
        for tr in result_tr:

            lista = tr.findAll("td")
            lista_inter = []

            for td in lista:
                lista_inter.append(td.text)
            
            lista_inter.extend([supermercado,categoria,desc_producto])
            lista_historico.append(lista_inter)

    df_historico_producto = pd.DataFrame(lista_historico)

    return df_historico_producto

async def load_datos_historico(lista_all_productos):

    start_time = time.time()

    df = pd.DataFrame()

    tareas = []

    for sup in lista_all_productos:
        for cat in sup:
            for prod in cat:
                tareas.append(get_historico(prod))

    lista_resultado_df = await asyncio.gather(*tareas)

    for i, r in enumerate(lista_resultado_df, 1):
            df = pd.concat([df, r])
            df.reset_index(drop=True, inplace=True)

    end_time = time.time()
    print(f"\n Total scrapeo de productos duró {end_time - start_time:.2f} segundos.")

    return df

def save_to_file(df):
    print(f"Numero de registros: {df.shape[0]}")
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    df.to_csv(f"../data/all_products_{fecha_hoy}.csv")
    print(f"Fichero Salvado: '../data/all_products_{fecha_hoy}.csv'") 


async def main():

    df = pd.DataFrame()

    lista_all_productos = get_list_productos(["https://super.facua.org/"])

    df = await load_datos_historico(lista_all_productos)

    df = df.rename(columns = {0: 'fecha', 
                    1: 'precio',
                    2: 'Variacion',
                    3: 'id_supermercado',
                    4: 'id_categoria',
                    5: 'desc_producto'})
    
    save_to_file(df)

    return df

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"\n Tiempo total del proceso: {end_time - start_time:.2f} segundos.")




