import pymysql
from decimal import Decimal

def calcular_monto_total():
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

            # Recuperar la información del tipo de combustible seleccionado
            cursor.execute("SELECT nombre, precio FROM tipo_combustible WHERE id = %s", (seleccion,))
            seleccionado = cursor.fetchone()

            if seleccionado:
                print(f"Has seleccionado {seleccionado[0]} - Precio por litro: Q{seleccionado[1]}")

                # Convertir el precio a float
                precio = float(seleccionado[1])

                # Solicitar al usuario la cantidad de litros
                while True:
                    try:
                        litros = float(input("Ingrese la cantidad de litros a despachar: "))
                        if litros <= 0:
                            print("La cantidad de litros debe ser un número positivo. Inténtelo de nuevo.")
                        else:
                            break
                    except ValueError:
                        print("Entrada no válida. Por favor, ingrese un número.")

                # Calcular el monto total
                monto_total = litros * precio
                print(f"El monto total a pagar es: Q{monto_total:.2f}")
            else:
                print("Selección inválida, por favor intente de nuevo.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        conexion.close()

# Llamar a la función para calcular el monto total
calcular_monto_total()
