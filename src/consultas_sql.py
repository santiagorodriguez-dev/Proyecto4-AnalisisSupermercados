

import pandas as pd # type: ignore
"""
Nos traemos todos los datos de las tablas, para poder analizar en dataframe

"""

def select_all_data(conn, cursor):
    try:

        query = """
        SELECT 
            p.id, p.fecha, p.precio, p.variacion, 
            s.nombre AS supermercado, 
            c.nombre AS categoria, 
            p.desc_producto
        FROM 
            productos_hist_precios p
        INNER JOIN 
            supermercados s ON p.id_supermercado = s.id
        INNER JOIN 
            categorias c ON p.id_categoria = c.id
        """
    
        cursor.execute(query)

        columnas = []

        for c in cursor.description:
            columnas.append(c[0])

        resultados = cursor.fetchall()

        df = pd.DataFrame(resultados,columns=columnas)

        return df
        
    except:
        print(f"Error en select_all_data(conn, cursor):")
    finally:
        if cursor:
            cursor.close()
        if conn:
           conn.close()