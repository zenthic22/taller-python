import pymysql

#Configuramos los parametros de la conexion
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'db_cursos'
}

#Intentaremos la conexion
try:
    conn = pymysql.connect(**config)
    print("Conexion exitosa")
    
    #Crearemos un cursor
    cursor = conn.cursor()
    
    #Ejecutaremos una consulta
    #cursor.execute("insert into cursos values (0772, 'Estructuras de Datos', 5);")
    #cursor.execute("delete from cursos where codigo=0772;")
    # cursor.execute("set SQL_SAFE_UPDATES = 0;")
    # cursor.execute("update cursos set nombre = 'EDD' where codigo = 0772;")
    # cursor.execute("insert into cursos values (0980, 'Proyectos aplicados a la IE', 6);")
    cursor.execute("set SQL_SAFE_UPDATES = 0;")
    cursor.execute("update cursos set nombre = 'Proyectos' where codigo = 0980;")
    #Confirmamos la transaccion
    conn.commit()
    
    cursor.execute("select * from cursos;")
    
    #Obtenemos los resultados
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)
        
except pymysql.MySQLError as err:
    print(f"Error: {err}")
    
finally:
    #Cerraremos el cursor
    if cursor:
        cursor.close()
    if conn:
        conn.close()