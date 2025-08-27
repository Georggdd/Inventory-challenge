import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="inventory",
        user="postgres",
        password="postgres"  
    )
    print("Conexión OK")
except Exception as e:
    print("Error al conectar:", e)
finally:
    if 'conn' in locals() and conn:
        conn.close()
