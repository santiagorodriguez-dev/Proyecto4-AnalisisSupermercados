# Importamos las librerías que necesitamos
# Beautifulsoup
from bs4 import BeautifulSoup

# Requests
import requests

import pandas as pd
import numpy as np

from time import sleep

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

def sacar_url_principales_supermercados(url):
    driver = webdriver.Chrome()
    url = "https://super.facua.org/"
    urls_super = []

    driver.get(url)
    driver.maximize_window()
    sleep(5)
    driver.find_element('css selector','#rcc-confirm-button').click()
    sleep(5)
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Acceder')

    for i in links:
        urls_super.append(i.get_attribute("href"))

    driver.close()

    return urls_super