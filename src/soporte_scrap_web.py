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
from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # Excepciones comunes de selenium que nos podemos encontrar
from selenium.webdriver.common.by import By

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

def main(input_data, texto):

    start_time = time.time()

    lista_total = []
    
    args = [(i, texto) for i in input_data]

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        resultados = pool.map(get_urls, args)

    for res in resultados:
        lista_total.append(res)
   
    end_time = time.time()
    print(f"\n el total duró {end_time - start_time:.2f} segundos.")
    
    return lista_total
