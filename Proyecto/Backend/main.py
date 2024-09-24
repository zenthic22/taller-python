from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import datetime
import smtplib
import pymysql
import bcrypt
import os
import openpyxl
import io

app = Flask(__name__)
CORS(app)

db_config = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='db_proyecto'
)

SECRET_KEY = os.urandom(24).hex()

def enviar_correo(destinatario, asunto, contenido):
    servidor_smtp = 'smtp.gmail.com'
    puerto = 587
    usuario = 'z07694496@gmail.com'
    password = 'kive hout kmgn pjpp'
    
    mensaje = MIMEMultipart()
    mensaje['From'] = usuario
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(contenido, 'plain'))
    
    try:
        with smtplib.SMTP(servidor_smtp, puerto) as server:
            server.starttls()
            server.login(usuario, password)
            server.sendmail(usuario, destinatario, mensaje.as_string())
        print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def rol_existe(rol_id):
    cursor = db_config.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM rol WHERE id = %s", (rol_id,))
        return cursor.fetchone()[0] > 0
    except Exception as e:
        print(f"Error al verificar rol: {e}")
        return False
    finally:
        cursor.close()

@app.route('/recuperar_password', methods=['POST'])
def recuperar_password():
    email = request.json.get('email')
    
    cursor = db_config.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    
    if usuario:
        token = jwt.encode({
            'user_id': usuario[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        
        reset_link = f'http://localhost:8000/restablecer_password/{token}'
        enviar_correo(email, 'Restablecer tu contraseña', f'Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}')
        
        return jsonify({"mensaje": "Se ha enviado un correo con el enlace para restablecer la contraseña."}), 200
    else:
        return jsonify({"error": "El correo no está registrado."}), 400
    
@app.route('/recuperar_password_catedratico', methods=['POST'])
def recuperar_password_catedratico():
    dpi = request.json.get('DPI')

    cursor = db_config.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE DPI = %s AND rol_id = 2", (dpi,))
    catedratico = cursor.fetchone()

    if catedratico:
        token = jwt.encode({
            'user_id': catedratico[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        reset_link = f'http://localhost:8000/restablecer_password_catedratico/{token}'
        enviar_correo('3508630320101@ingenieria.usac.edu.gt', 'Restablecer contraseña catedrático', 
                      f'Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}')
        
        return jsonify({"mensaje": "Se ha enviado un correo con el enlace para restablecer la contraseña."}), 200
    else:
        return jsonify({"error": "El DPI no está registrado."}), 400

@app.route('/actualizar_password', methods=['POST'])
def restablecer_password():
    token = request.json.get('token')
    nueva_password = request.json.get('nueva_password')

    if not nueva_password:
        return jsonify({"error": "La nueva contraseña es requerida."}), 400
    
    if len(nueva_password) < 8:
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres."}), 400

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = data['user_id']

        hashed_password = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())

        cursor = db_config.cursor()
        cursor.execute("UPDATE Usuario SET password = %s WHERE id = %s", (hashed_password, user_id))
        db_config.commit()

        return jsonify({"mensaje": "Contraseña restablecida exitosamente."}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "El enlace ha expirado."}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido."}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500

@app.route('/registro', methods=['POST'])
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
    rol_id = datos.get('rol_id')

    if not rol_existe(rol_id):
        return jsonify({"error": "Rol no válido"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor = db_config.cursor()
    
    try:
        cursor.execute(""" 
            INSERT INTO Usuario (nombre, apellido, DPI, fecha_nacimiento, telefono, nombre_usuario, email, password, rol_id, login_attempts, account_locked)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 0, FALSE)
        """, (nombre, apellido, dpi, fecha_nacimiento, telefono, nombre_usuario, email, hashed_password, rol_id))

        db_config.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 200
    except Exception as e:
        db_config.rollback()
        print(f"Error al insertar datos: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
    
@app.route('/registro_catedratico', methods=['POST'])
def registrar_catedratico():
    datos = request.json

    nombre = datos.get('nombre')
    apellido = datos.get('apellido')
    dpi = datos.get('DPI')
    password = datos.get('password')

    if not all([nombre, apellido, dpi, password]):
        return jsonify({"error": "Faltan campos requeridos."}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor = db_config.cursor()
    
    try:
        cursor.execute(""" 
            INSERT INTO Usuario (nombre, apellido, DPI, password, rol_id, login_attempts, account_locked)
            VALUES (%s, %s, %s, %s, %s, 0, FALSE)
        """, (nombre, apellido, dpi, hashed_password, 2))

        db_config.commit()
        return jsonify({"mensaje": "Catedrático registrado exitosamente"}), 200
    except Exception as e:
        db_config.rollback()
        print(f"Error al insertar datos: {e}")
        return jsonify({"error": str(e)}), 400
    
@app.route('/login', methods=['POST'])
def iniciar_sesion():
    datos = request.json
    nombre_usuario = datos.get('nombre_usuario')
    dpi = datos.get('DPI')
    email = datos.get('email')
    password = datos.get('password').encode('utf-8')

    cursor = db_config.cursor(pymysql.cursors.DictCursor)

    if nombre_usuario:
        cursor.execute("SELECT * FROM Usuario WHERE nombre_usuario = %s", (nombre_usuario,))
    elif dpi:
        cursor.execute("SELECT * FROM Usuario WHERE DPI = %s", (dpi,))
    elif email:
        cursor.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
    else:
        return jsonify({"mensaje": "Falta el nombre de usuario, DPI o email."}), 400

    usuario = cursor.fetchone()

    if not usuario:
        return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

    if usuario['account_locked']:
        return jsonify({"mensaje": "Cuenta bloqueada. Contacte al administrador."}), 403

    if bcrypt.checkpw(password, usuario['password'].encode('utf-8')):
        cursor.execute("UPDATE Usuario SET login_attempts = 0 WHERE id = %s", (usuario['id'],))
        db_config.commit()
        return jsonify({"mensaje": "Inicio de sesión exitoso", 
                        "rol_id": usuario['rol_id'],
                        "nombre": usuario['nombre']}), 200
    else:
        cursor.execute("UPDATE Usuario SET login_attempts = login_attempts + 1 WHERE id = %s", (usuario['id'],))
        db_config.commit()

        if usuario['login_attempts'] >= 2:
            cursor.execute("UPDATE Usuario SET account_locked = TRUE WHERE id = %s", (usuario['id'],))
            db_config.commit()
            return jsonify({"mensaje": "Cuenta bloqueada. Contacte al administrador."}), 403
        
        return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

@app.route('/descargar_listado_catedraticos')
def descargar_listado_catedraticos():
    cursor = db_config.cursor()
    cursor.execute("SELECT nombre, apellido, DPI FROM Usuario WHERE rol_id = 2")
    catedraticos = cursor.fetchall()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Nombre", "Apellido", "DPI"])

    for catedratico in catedraticos:
        sheet.append(catedratico)

    stream = io.BytesIO()
    workbook.save(stream)
    stream.seek(0)

    return send_file(stream, as_attachment=True, download_name="catedraticos.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.route('/listado_usuarios_bloqueados', methods=['GET'])
def listado_usuarios_bloqueados():
    cursor = db_config.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, nombre, apellido, DPI, rol_id FROM Usuario WHERE account_locked = TRUE")
    usuarios_bloqueados = cursor.fetchall()
    return jsonify(usuarios_bloqueados), 200

@app.route('/desbloquear/<int:usuario_id>', methods=['POST'])
def desbloquear_usuario(usuario_id):
    cursor = db_config.cursor()

    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT * FROM Usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado."}), 404
        
        # Desbloquear el usuario y reiniciar login_attempts
        cursor.execute("UPDATE Usuario SET account_locked = FALSE, login_attempts = 0 WHERE id = %s", (usuario_id,))
        db_config.commit()

        return jsonify({"mensaje": "Usuario desbloqueado exitosamente."}), 200

    except Exception as e:
        db_config.rollback()  # Hacer rollback en caso de error
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)