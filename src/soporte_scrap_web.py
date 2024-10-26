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

import sys
sys.path.append("../")
from src import soporte as sp


def get_urls(input_data):
    """
    Obtiene una lista de URLs que contienen un texto parcial específico en sus enlaces, 
    accediendo a una página web dada.

    Args:
        input_data (list): Una lista que contiene dos elementos:
            - El primer elemento es la URL de la página web a la que se accederá.
            - El segundo elemento es el texto parcial que se buscará en los enlaces de la página.

    Returns:
        list: Una lista de cadenas que representan las URLs de los enlaces que contienen 
        el texto parcial especificado. Si ocurre un error, se imprime un mensaje de error 
        y se devuelve una lista vacía.

    Raises:
        No levanta explícitamente excepciones, pero imprime "error en get_urls(input_data)" 
        en caso de fallar en cualquier punto.

    Utiliza Selenium para abrir un navegador, maximizar la ventana, aceptar cookies si es 
    necesario, y buscar enlaces que contengan el texto parcial especificado. Finalmente, 
    cierra el navegador y devuelve la lista de URLs.
    """
    
    urls_return = []
    try:
        driver = webdriver.Chrome()
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
    except:
        print("error en get_urls(input_data)")

    return urls_return

def procesar(input_data, texto):
    """
    Procesa una lista de datos de entrada para obtener múltiples listas de URLs en paralelo, 
    utilizando múltiples núcleos de CPU.

    Args:
        input_data (list): Una lista de elementos, donde cada elemento será utilizado como 
        argumento para la función `get_urls`.
        texto (str): El texto parcial que se buscará en los enlaces de cada URL proporcionada 
        en `input_data`.

    Returns:
        list: Una lista de listas, donde cada sublista contiene las URLs obtenidas de la 
        función `get_urls` para cada entrada en `input_data`. Si ocurre un error, se imprime 
        un mensaje de error y se devuelve una lista vacía.

    Raises:
        No levanta explícitamente excepciones, pero imprime "error en procesar(input_data, texto)" 
        en caso de fallar en cualquier punto.

    Utiliza `multiprocessing` para realizar el procesamiento en paralelo, asignando tareas a 
    todos los núcleos de CPU disponibles. Llama a la función `get_urls` para cada par (input_data[i], texto).
    """

    retun_list = []

    try:
        args = [(i, texto) for i in input_data]

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            resultados = pool.map(get_urls, args)

        for res in resultados:
            retun_list.append(res)
    except:
        print("error en procesar(input_data, texto)")
       
    return retun_list

def get_list_productos(url_first):
    """
    Obtiene una lista de productos mediante la recopilación de URLs de varias categorías
    en un sitio web, a partir de una lista inicial de URLs.

    Args:
        url_first (list): Una lista de URLs iniciales que serán procesadas para obtener enlaces de 
        supermercados y sus respectivas categorías de productos.

    Returns:
        list: Una lista de listas anidadas que contienen URLs de productos extraídas de las categorías y 
        subcategorías. Si ocurre un error, se imprime un mensaje de error y se devuelve una lista vacía.

    Raises:
        No levanta explícitamente excepciones, pero imprime "error en get_list_productos(url_first)" 
        en caso de fallar en cualquier punto.

    Este método realiza lo siguiente:
        1. Llama a la función `procesar` para obtener los enlaces de acceso a los supermercados a partir 
           de las URLs iniciales.
        2. Procesa los enlaces para obtener las categorías de productos en cada supermercado.
        3. Obtiene las subcategorías y los enlaces históricos de productos.
        4. Mide el tiempo total de ejecución e imprime el tiempo transcurrido para el proceso completo.
    """

    lista_all_productos = []
    try:
        start_time = time.time()

        list_urls_super = procesar(url_first,"Acceder")

        list_con_categorias=[]

        for supermecados in list_urls_super:
            list_con_categorias.append(procesar(supermecados,'Ver'))

        for k in list_con_categorias:
            for h in k:
                lista_all_productos.append(procesar(h,'Histórico'))

        
        end_time = time.time()
        print(f"\n Total scrapeo de urls duró {end_time - start_time:.2f} segundos.")

    except:
        print("error en get_list_productos(url_first)")

    return lista_all_productos

async def get_historico(url):
    """
    Extrae y organiza datos históricos de precios de productos de una página web y 
    devuelve los resultados en un DataFrame de pandas.

    Args:
        url (str): La URL de la página web que contiene la tabla de datos históricos del 
        producto.

    Returns:
        pd.DataFrame: Un DataFrame que contiene los datos históricos de los productos. 
        Cada fila representa un registro con información de precio, fecha, supermercado, 
        categoría y descripción del producto. Si ocurre un error, se imprime un mensaje de 
        error y se devuelve un DataFrame vacío.

    Raises:
        No levanta explícitamente excepciones, pero imprime "error en get_historico(url)" 
        en caso de fallar en cualquier punto.

    Este método realiza lo siguiente:
        1. Realiza una solicitud HTTP GET a la URL proporcionada.
        2. Analiza el contenido HTML para extraer una tabla con datos históricos de precios.
        3. Identifica el supermercado, la categoría y la descripción del producto a partir de la URL.
        4. Construye una lista con los datos históricos y la convierte en un DataFrame.
    """

    df_historico_producto = pd.DataFrame()

    try:
        url_sopa = url

        res = requests.get(url_sopa)
        sopa = BeautifulSoup(res.content, "html.parser")

        resultado = sopa.find("tbody")
        result_tr = resultado.findAll("tr")
        
        if (res.status_code == 200 and resultado and result_tr):
            datos = url.split("/")[3:6]
            supermercado = ''
            categoria = ''
            desc_producto = str(datos[2]).replace('-',' ')

            for x, y in sp.supermercados_dicc.items():
                if (str(datos[0]).replace('-',' ') == x):
                    supermercado = y
            
            for x, y in sp.categorias_dicc.items():
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

    except:
        print("error en get_historico(url)")
 
    return df_historico_producto

async def load_datos_historico(lista_all_productos):
    """
    Carga los datos históricos de precios de productos a partir de una lista de URLs y 
    devuelve un DataFrame consolidado.

    Args:
        lista_all_productos (list): Una lista anidada de URLs, donde cada nivel representa 
        la estructura jerárquica de supermercado, categoría y producto.

    Returns:
        pd.DataFrame: Un DataFrame que contiene los datos históricos de precios de todos los 
        productos extraídos. Cada fila corresponde a un registro de datos con información 
        sobre el precio, la fecha, el supermercado, la categoría y la descripción del producto. 
        Si ocurre un error, se imprime un mensaje de error y se devuelve un DataFrame vacío.

    Raises:
        No levanta explícitamente excepciones, pero imprime "error en load_datos_historico(lista_all_productos)" 
        en caso de fallar en cualquier punto.

    Este método realiza lo siguiente:
        1. Crea tareas asincrónicas para obtener datos históricos de cada producto mediante 
           la función `get_historico`.
        2. Utiliza `asyncio.gather` para ejecutar las tareas en paralelo y recolecta los 
           resultados en una lista de DataFrames.
        3. Concatena los DataFrames no vacíos en un solo DataFrame consolidado.
        4. Mide el tiempo total de ejecución e imprime el tiempo transcurrido para el proceso completo.
    """

    df = pd.DataFrame()
    try:
        start_time = time.time()

        tareas = []

        for sup in lista_all_productos:
            for cat in sup:
                for prod in cat:
                    tareas.append(get_historico(prod))

        lista_resultado_df = await asyncio.gather(*tareas)

        for i, r in enumerate(lista_resultado_df, 1):
                if (r.empty == False):
                    df = pd.concat([df, r])
                    df.reset_index(drop=True, inplace=True)

        end_time = time.time()
        print(f"\n Total scrapeo de productos duró {end_time - start_time:.2f} segundos.")

    except:
        print("error en load_datos_historico(lista_all_productos)")

    return df

def save_to_file(df):
    """
    Guarda un DataFrame en un archivo CSV y muestra información sobre el número de registros.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos que se guardarán en el archivo CSV.

    Returns:
        None: La función no devuelve ningún valor, pero guarda un archivo CSV y muestra 
        información en la consola.

    Este método realiza lo siguiente:
        1. Imprime el número de registros en el DataFrame.
        2. Genera un nombre de archivo basado en la fecha actual en el formato 'YYYY-MM-DD'.
        3. Guarda el DataFrame como un archivo CSV en la ruta '../data/', utilizando el 
           nombre generado.
        4. Imprime un mensaje indicando la ruta del archivo guardado.
    """
    print(f"Numero de registros: {df.shape[0]}")
    fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    df.to_csv(f"../data/all_products_{fecha_hoy}.csv")
    print(f"Fichero Salvado: '../data/all_products_{fecha_hoy}.csv'") 


async def main():
    """
    Función principal que ejecuta el flujo completo de obtención, procesamiento y almacenamiento 
    de datos históricos de productos.

    Returns:
        pd.DataFrame: Un DataFrame que contiene los datos históricos de productos con columnas 
        renombradas. Cada fila incluye la fecha, precio, variación, identificadores de supermercado 
        y categoría, y la descripción del producto.

    Este método realiza lo siguiente:
        1. Llama a la función `get_list_productos` para obtener una lista de URLs de productos.
        2. Utiliza la función `load_datos_historico` para cargar los datos históricos de precios 
           de los productos de manera asincrónica.
        3. Renombra las columnas del DataFrame para hacerlas más descriptivas.
        4. Guarda el DataFrame en un archivo CSV mediante la función `save_to_file`.
        5. Devuelve el DataFrame consolidado.
    """

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




