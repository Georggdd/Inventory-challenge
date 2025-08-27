"""
Script de prueba para verificar la conexión a la base de datos PostgreSQL.
Intenta conectarse y cierra la conexión automáticamente.
"""

import psycopg2

try:
    # Intentar conectar a la base de datos con los parámetros indicados
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="inventory",
        user="postgres",
        password="postgres"  
    )
    print("Conexión OK")  # Confirmación de conexión exitosa
except Exception as e:
    print("Error al conectar:", e)  # Mostrar cualquier error de conexión
finally:
    # Cerrar la conexión si se abrió
    if 'conn' in locals() and conn:
        conn.close()
