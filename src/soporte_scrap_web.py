# Importamos las librerías que necesitamos

# Librerías de extracción de actividades
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore

# Tratamiento de actividades
# -----------------------------------------------------------------------
import pandas as pd # type: ignore
import numpy as np
import re
from time import sleep
import time
import multiprocessing

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

    with multiprocessing.Pool(processes=4) as pool:
        resultados = pool.map(get_urls, args)

    for res in resultados:
        retun_list.append(res)
   
    return retun_list

def main(url_first):

    start_time = time.time()

    lista_all_productos = []

    url_first = ["https://super.facua.org/"]

    list_urls_super = procesar(url_first,"Acceder")

    list_con_categorias=[]

    for super in list_urls_super:
        list_con_categorias.append(procesar(super,'Ver'))

    for k in list_con_categorias:
        for h in k:
            lista_all_productos.append(procesar(h,'Histórico'))

    
    end_time = time.time()
    print(f"\n Total scrapeo de urls duró {end_time - start_time:.2f} segundos.")

    return lista_all_productos
