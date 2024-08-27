import pymysql

def mostrar_opciones_combustible():
    # Conectar a la base de datos
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="combustible"
    )

    try:
        with conexion.cursor() as cursor:
            # Recuperar y mostrar los tipos de combustible
            cursor.execute("SELECT id, nombre, precio FROM tipo_combustible")
            combustibles = cursor.fetchall()

            print("Seleccione un tipo de combustible:")
            for combustible in combustibles:
                print(f"{combustible[0]}. {combustible[1]} - Precio por litro: Q{combustible[2]}")

            # Solicitar al usuario que seleccione un tipo de combustible
            seleccion = int(input("Ingrese el número correspondiente al tipo de combustible: "))

            # Mostrar el tipo de combustible seleccionado y su precio
            cursor.execute("SELECT nombre, precio FROM tipo_combustible WHERE id = %s", (seleccion,))
            seleccionado = cursor.fetchone()

            if seleccionado:
                print(f"Has seleccionado {seleccionado[0]} - Precio por litro: Q{seleccionado[1]}")
            else:
                print("Selección inválida, por favor intente de nuevo.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        conexion.close()

# Llamar a la función para mostrar las opciones de combustible
mostrar_opciones_combustible()
