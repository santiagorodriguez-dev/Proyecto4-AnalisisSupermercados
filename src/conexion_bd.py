
import psycopg2 # type: ignore

def create_connection(DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME):
    """
    Crea una conexión a la base de datos PostgreSQL.

    Returns:
        conn (psycopg2.extensions.connection): Objeto de conexión a la base de datos.
        cursor (psycopg2.extensions.cursor): Cursor para ejecutar consultas en la base de datos.

    Raises:
        Exception: Si hay un error al intentar conectarse a la base de datos.
    """
    try:
        # Obtener las credenciales desde las variables de entorno
        user = DB_USER
        password = DB_PASSWORD
        host =DB_HOST
        port = DB_PORT
        database = DB_NAME

        # Crear la conexión
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

        cursor = conn.cursor()
        print("Conexión a la base de datos establecida con éxito.")
        return conn, cursor

    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        raise

def close_connection(conn, cursor):
    """
    Cierra la conexión a la base de datos PostgreSQL.

    Args:
        conn (psycopg2.extensions.connection): Objeto de conexión a la base de datos.
        cursor (psycopg2.extensions.cursor): Cursor de la base de datos.
    """
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Conexión a la base de datos cerrada con éxito.")
