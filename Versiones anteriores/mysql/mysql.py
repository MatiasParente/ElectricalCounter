
import MySQLdb

# Intenta conectar a MySQL
try:
    connection = MySQLdb.connect(
        host='192.168.192.2',
        user='aplicacion',
        password='Qwerty123#',
        db='Proyecto'
    )
    print("Conexión exitosa a MySQL")

    # Crear un cursor para interactuar con la base de datos
    cursor = connection.cursor()

    # Ejecutar una consulta SELECT
    cursor.execute("SELECT * FROM Dato")

    # Obtener todos los resultados de la consulta
    resultados = cursor.fetchall()

    # Imprimir los resultados
    for fila in resultados:
        print(fila)

except Exception as e:
    print("Error al conectar a MySQL:", e)
finally:
        if connection:
            # Cerrar el cursor y la conexión
            cursor.close()
            connection.close()
