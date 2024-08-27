import pymysql

def conectar_bd():
    try:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="combustible"
        )
    except pymysql.MySQLError as e:
        print(f"No se pudo conectar a la base de datos: {e}")
        return None

def obtener_numero(prompt):
    while True:
        try:
            numero = float(input(prompt))
            if numero <= 0:
                print("El número debe ser positivo. Inténtelo de nuevo.")
            else:
                return numero
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número válido.")

def escribir_factura(resumen):
    try:
        with open("facturas.txt", "a") as archivo:
            archivo.write(resumen + "\n")
    except IOError as e:
        print(f"No se pudo escribir en el archivo facturas.txt: {e}")

def generar_factura():
    conexion = conectar_bd()
    if conexion is None:
        return

    try:
        with conexion.cursor() as cursor:
            # Ingresar datos del cliente
            nombre_cliente = input("Ingrese el nombre del cliente: ")
            placa = input("Ingrese la identificación del vehículo (por ejemplo, número de placa): ")

            # Guardar los datos del cliente en la base de datos
            try:
                cursor.execute("INSERT INTO clientes (nombre, placa) VALUES (%s, %s)",
                               (nombre_cliente, placa))
                conexion.commit()
            except pymysql.MySQLError as e:
                print(f"Error al guardar los datos del cliente: {e}")
                return

            # Recuperar y mostrar los tipos de combustible
            try:
                cursor.execute("SELECT id, nombre, precio FROM tipo_combustible")
                combustibles = cursor.fetchall()
            except pymysql.MySQLError as e:
                print(f"Error al recuperar los tipos de combustible: {e}")
                return

            print("Seleccione un tipo de combustible:")
            for combustible in combustibles:
                print(f"{combustible[0]}. {combustible[1]} - Precio por litro: Q{combustible[2]}")

            # Solicitar al usuario que seleccione un tipo de combustible
            seleccion = int(obtener_numero("Ingrese el número correspondiente al tipo de combustible: "))

            # Recuperar la información del tipo de combustible seleccionado
            try:
                cursor.execute("SELECT nombre, precio FROM tipo_combustible WHERE id = %s", (seleccion,))
                seleccionado = cursor.fetchone()
                if not seleccionado:
                    print("Selección inválida, por favor intente de nuevo.")
                    return
            except pymysql.MySQLError as e:
                print(f"Error al recuperar la información del tipo de combustible seleccionado: {e}")
                return

            print(f"Has seleccionado {seleccionado[0]} - Precio por litro: Q{seleccionado[1]}")

            # Convertir el precio a float
            precio = float(seleccionado[1])

            # Solicitar al usuario la cantidad de litros
            litros = obtener_numero("Ingrese la cantidad de litros a despachar: ")

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
            escribir_factura(resumen)
            print("Factura generada y almacenada en facturas.txt")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        conexion.close()

if __name__ == "__main__":
    generar_factura()
