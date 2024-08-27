import pymysql
from decimal import Decimal

def generar_factura():
    # Conectar a la base de datos
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="combustible"
    )

    try:
        with conexion.cursor() as cursor:
            # Ingresar datos del cliente
            nombre_cliente = input("Ingrese el nombre del cliente: ")
            placa = input("Ingrese la identificación del vehículo (por ejemplo, número de placa): ")

            # Guardar los datos del cliente en la base de datos
            cursor.execute("INSERT INTO clientes (nombre, placa) VALUES (%s, %s)",
                           (nombre_cliente, placa))
            conexion.commit()

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

                # Generar el resumen de la transacción
                resumen = (f"Factura:\n"
                           f"Nombre del Cliente: {nombre_cliente}\n"
                           f"Identificación del Vehículo: {placa}\n"
                           f"Tipo de Combustible: {seleccionado[0]}\n"
                           f"Cantidad de Litros: {litros}\n"
                           f"Precio por Litro: Q{precio}\n"
                           f"Monto Total a Pagar: Q{monto_total:.2f}\n")

                print(resumen)

                # Almacenar la información en un archivo de texto
                with open("facturas.txt", "a") as archivo:
                    archivo.write(resumen + "\n")
                    print("Factura generada y almacenada en facturas.txt")

            else:
                print("Selección inválida, por favor intente de nuevo.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        conexion.close()

# Llamar a la función para generar la factura
generar_factura()
