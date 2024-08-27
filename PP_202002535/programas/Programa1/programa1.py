import pymysql

def ingresar_datos_cliente():
    conexion = pymysql.connect(
        host="localhost",
        user="root", #cambias user
        password="root", #cambias pass
        database="cliente_vehiculo" #cambias el nombre
    )
    
    try:
        with conexion.cursor() as cursor:
            nombre_cliente = input("Ingrese el nombre: ")
            placa_vehiculo = input("Ingrese la placa: ")
            
            consulta = "insert into Cliente (nombre_cliente, placa) values (%s, %s)"
            valores = (nombre_cliente, placa_vehiculo)
            
            cursor.execute(consulta, valores)
            conexion.commit()
            
            print("Datos del cliente ingresados correctamente.")
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        conexion.close()
        
ingresar_datos_cliente()