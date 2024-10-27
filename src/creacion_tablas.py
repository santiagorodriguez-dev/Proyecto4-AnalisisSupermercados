

import pandas as pd # type: ignore
import sys
sys.path.append("../")
from src import soporte as sp

def create_table_supermercados(conn, cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS supermercados (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        conn.commit()
        print("Tabla 'supermercados' creada con éxito.")
    except:
        print(f"Error al crear la tabla: supermercados")
    
def insert_supermercados(conn, cursor):
    """
    Inserta los supermercados del diccionario en la tabla 'supermercados'.
    """
    try:
        for nombre, id in sp.supermercados_dicc.items():
            cursor.execute("""
                INSERT INTO supermercados (id, nombre) VALUES (%s, %s)
                ON CONFLICT (nombre) DO NOTHING
            """, (id, nombre))
        conn.commit()
        print("Supermercados insertados con éxito.")
    except Exception as e:
        print(f"Error al insertar los supermercados: {e}")

def create_table_categorias(conn, cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        conn.commit()
        print("Tabla 'categorias' creada con éxito.")
    except:
        print(f"Error al crear la tabla: categorias")
    
def insert_categorias(conn, cursor):
    """
    Inserta las categorias del diccionario en la tabla 'categorias'.
    """
    try:
        for nombre, id in sp.categorias_dicc.items():
            cursor.execute("""
                INSERT INTO categorias (id, nombre) VALUES (%s, %s)
                ON CONFLICT (nombre) DO NOTHING
            """, (id, nombre))
        conn.commit()
        print("categorias insertados con éxito.")
    except:
        print(f"Error al insertar los categorias")

def create_table_productos_hist_precios(conn, cursor):
    try:
    
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos_hist_precios (
                id SERIAL PRIMARY KEY,
                fecha DATE NOT NULL,
                precio DECIMAL(10, 2) NOT NULL,
                variacion VARCHAR(100),
                id_supermercado INTEGER NOT NULL,
                id_categoria INTEGER NOT NULL,
                desc_producto VARCHAR(255) NOT NULL,
                FOREIGN KEY (id_supermercado) REFERENCES supermercados (id),
                FOREIGN KEY (id_categoria) REFERENCES categorias (id)
            )
        """)
        conn.commit()
        print("Tabla 'productos_hist_precios' creada con éxito.")
    except:
        print(f"Error al crear la tabla 'productos_hist_precios")


def insert_data_productos_hist_precios(conn, cursor, df):
    """
    Carga un DataFrame en la tabla 'productos_hist_precios'.
    """
    try:
        for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO productos_hist_precios (fecha, precio, variacion, id_supermercado, id_categoria, desc_producto)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    pd.to_datetime(row['fecha'], format='%d/%m/%Y').date(), 
                    float(row['precio'].replace(',', '.')),
                    row['Variacion'],
                    row['id_supermercado'],
                    row['id_categoria'],
                    row['desc_producto']
                ))
        conn.commit()
        print("Datos cargados con éxito en la tabla 'productos_hist_precios'.")
    except :
        print(f"Error al cargar datos en la tabla: productos_hist_precios")


def main(conn, cursor, df):
    create_table_supermercados(conn,cursor)

    insert_supermercados(conn,cursor)

    create_table_categorias(conn,cursor)

    insert_categorias(conn,cursor)

    create_table_productos_hist_precios(conn,cursor)

    insert_data_productos_hist_precios(conn,cursor,df)

    

