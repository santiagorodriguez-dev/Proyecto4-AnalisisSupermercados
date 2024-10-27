# Proyecto: Análisis de Precios de Supermercados

## Descripción General

La página [FACUA: Precios Supermercados](https://super.facua.org/) proporciona información actualizada sobre los precios de productos básicos en seis grandes supermercados de España: Alcampo, Carrefour, Dia, Eroski, Hipercor y Mercadona. Los usuarios pueden comparar precios de productos como aceite y leche, observar la evolución de precios en diferentes fechas, y ver las mayores subidas de precios recientes. La plataforma revisa a diario la evolución de los precios, permitiendo a los consumidores estar informados sobre las fluctuaciones y posibles abusos en los precios.

## Objetivos Específicos

**Scraping de datos**: Extraer información detallada de todos los productos disponibles en la web de FACUA para cada uno de los supermercados listados.
**Extraccion de datos**: Se ha extraido dinamicamente las urls de todos los supermercados.
<div style="text-align: center;">
  <img src="https://github.com/santiagorodriguez-dev/Proyecto4-AnalisisSupermercados/blob/main/images/listado_super.PNG" alt="esquema" />
</div>

**Extraccion de datos**: Se ha extraido dinamicamente las urls de las categorias de todos los supermercados.

<div style="text-align: center;">
  <img src="https://github.com/santiagorodriguez-dev/Proyecto4-AnalisisSupermercados/blob/main/images/categorias.PNG" alt="esquema" />
</div>

**Almacenamiento en base de datos**: Crear una base de datos en SQL que almacene la información recolectada de manera estructurada.
**Estructura de BD**: Se han creado tres tablas con los datos de supermercados, categorias y productos.
<div style="text-align: center;">
  <img src="https://github.com/santiagorodriguez-dev/Proyecto4-AnalisisSupermercados/blob/main/images/diagrama.PNG" alt="esquema" />
</div>

### Analisis de datos: Graficos sobre diferentes comparaciones de precios.

#### Comparación de Precios entre Supermercados por las diferentes categorias para todos los datos extraidos

<div style="text-align: center;">
  <img src="https://github.com/santiagorodriguez-dev/Proyecto4-AnalisisSupermercados/blob/main/images/01.png" alt="esquema" />
</div>

#### Conclusion:
Observamos que dia, eroski y mercadona tienes los precios promedio mas bajos.


#### Comparación de Precios entre Supermercados por las diferentes categorias, por precio maximo y minimo

<div style="text-align: center;">
  <img src="https://github.com/santiagorodriguez-dev/Proyecto4-AnalisisSupermercados/blob/main/images/02.png" alt="esquema" />
</div>

#### Conclusion:
Observamos que dia, mercadona tienes los precios globales de todos los productos maximos mas bajos que el resto de supermercados.

#### Análisis de la Evolución de Precios por supermercado y la categoria leche**
 
<div style="text-align: center;">
  <img src="https://github.com/santiagorodriguez-dev/Proyecto4-AnalisisSupermercados/blob/main/images/03.png" alt="esquema" />
</div>

#### Conclusion:
Observamos que carrefour, tiene un pico estacional en el precio promedio de la leche. posiblemente por que en la categoria de leche tambien se incluyen productos
para proteger del sol en verano. Ademas vemos que eroski e hipercor, tienen los precios promedio mas bajos, con mucha diferencia.

#### Análisis de la Evolución de Precios por supermercado y la categoria aceite de girasol**
  
<div style="text-align: center;">
  <img src="https://github.com/santiagorodriguez-dev/Proyecto4-AnalisisSupermercados/blob/main/images/04.png" alt="esquema" />
</div>

#### Conclusion:
El precio promedio se mantiene en todos los supermercados. Observamos que eroski, hipercor y mercadona, tienen los precios promedio mas bajos.

#### Análisis de la Evolución de Precios por supermercado y la categoria aceite de oliva
  
<div style="text-align: center;">
  <img src="https://github.com/santiagorodriguez-dev/Proyecto4-AnalisisSupermercados/blob/main/images/05.png" alt="esquema" />
</div>

#### Conclusion:
El precio promedio se mantiene en todos los supermercados salvo en carrefour que se ve una tendencia estacional que baja el promedio para luego subir. Observamos que eroski, dia y mercadona, tienen los precios promedio mas bajos.
  
## Conclusiones Finales:
   - Con los datos analizados, observamos patrones de modficaciones de precios, aparentemente injustificados en carrefour. los demas supermercados no tienen esas variaciones.
   - Por otro lado vemos que el supermercado con precios promedios mas bajos en todas las categorias es eroski.

#### Propuestas de Mejora:
   - Analisis mas profundo en la segmentacion de productos por cantidad de los mismos, eso daria un analisis mas exacto.
  
## Construido con 🛠️

* [Pyhton](https://www.python.org/) - Lenguaje utilizado
* [Numpy](https://numpy.org/doc/stable/) - Numpy
* [seaborn](https://seaborn.pydata.org/tutorial.html) - Seaborn
* [matplotlib](https://matplotlib.org/stable/users/index) - matplotlib
* [pandas](https://pandas.pydata.org/docs/) - pandas
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - BeautifulSoup
* [selenium](https://www.selenium.dev/documentation/) - selenium
* [Visual Studio Code](https://code.visualstudio.com/) - IDE desarrollo
  
## Autores ✒️

* **Santiago Rodriguez** - [santiagorodriguez-dev](https://github.com/santiagorodriguez-dev)
