from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import bcrypt
import pymysql.cursors

app = Flask(__name__)
CORS(app)

db_config = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='db_proyecto'
)

# Verificar si un rol existe
def rol_existe(rol_id):
    cursor = db_config.cursor()
    cursor.execute("SELECT COUNT(*) FROM rol WHERE id = %s", (rol_id,))
    return cursor.fetchone()[0] > 0

@app.route('/registro', methods=['POST']) #post, get, put, delete
def registrar_usuario():
    datos = request.json
    nombre = datos.get('nombre')
    apellido = datos.get('apellido')
    dpi = datos.get('DPI')
    fecha_nacimiento = datos.get('fecha_nacimiento')
    telefono = datos.get('telefono')
    nombre_usuario = datos.get('nombre_usuario')
    email = datos.get('email')
    password = datos.get('password')
    rol_id = datos.get('rol_id')  # 1. Administrador, 2. Catedratico, Alumno
    
    # Comprobar si el rol existe
    if not rol_existe(rol_id):
        return jsonify({"error": "El rol especificado no existe."}), 400
    
    # Codifica la contraseña antes de usarla
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor = db_config.cursor()
    
    try:
        # Inserta los datos
        cursor.execute(""" 
            insert into Usuario (nombre, apellido, DPI, fecha_nacimiento, telefono, nombre_usuario, email, password, rol_id)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, dpi, fecha_nacimiento, telefono, nombre_usuario, email, hashed_password, rol_id))

        db_config.commit()
        print(nombre, apellido, dpi, fecha_nacimiento, telefono, nombre_usuario, email, hashed_password, rol_id)
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 200
    except Exception as e:
        db_config.rollback()
        print(f"Error al insertar datos: {e}")
        return jsonify({"error": str(e)}), 400
    
@app.route('/login', methods=['POST'])
def iniciar_sesion():
    datos = request.json
    nombre_usuario = datos.get('nombre_usuario')
    password = datos.get('password').encode('utf-8')
    
    cursor = db_config.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from Usuario where nombre_usuario = %s", (nombre_usuario,))
    usuario = cursor.fetchone()
    
    if usuario and bcrypt.checkpw(password, usuario['password'].encode('utf-8')):
        return jsonify({"mensaje": "Inicio de sesión exitoso", "rol_id": usuario['rol_id']}), 200
    else:
        return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

@app.route('/logout', methods=['GET'])
def cerrar_sesion():
    return jsonify({"mensaje": "Sesión cerrada exitosamente"}), 200
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)