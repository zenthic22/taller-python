import requests
import base64
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm, LoginForm, RegistroCatedraticoForm, CursoForm

endpoint = 'http://localhost:3000'

def home(request):
    contexto = {'tab': 'Inicio'}
    response = requests.get(endpoint)
    return render(request, 'index.html', contexto)

def login(request):
    contexto = {
        'tab': 'Iniciar Sesión',
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido'),
        'form': LoginForm()  # Crea una instancia del formulario
    }
    
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Pasa los datos del POST al formulario
        
        if form.is_valid():  # Verifica si el formulario es válido
            usuario_input = form.cleaned_data['usuario']  # Obtiene la entrada del usuario
            password = form.cleaned_data['password']  # Obtiene la contraseña
            
            datos = {
                'nombre_usuario': usuario_input,
                'DPI': usuario_input,  # Se pasará el mismo valor, pero el servidor decidirá cuál usar
                'password': password,
            }

            response = requests.post(f'{endpoint}/login', json=datos)
            if response.status_code == 200:
                usuario = response.json()
                request.session['nombre_usuario'] = usuario.get('nombre', 'usuario desconocido')
                rol_id = usuario.get('rol_id')
                return redirect({
                    1: 'vista_administrador',
                    2: 'vista_catedratico',
                    3: 'vista_alumno'
                }.get(rol_id, 'login'))  # Redirigir según rol
            elif response.status_code == 403:
                messages.error(request, 'Cuenta bloqueada. Contacte al administrador.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
            
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    
    return render(request, 'login.html', contexto)

def registro(request):
    contexto = {'tab': 'Registro de Usuario'}

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'registro.html', {'form': form, **contexto})

            datos = {
                'nombre': form.cleaned_data['nombre'],
                'apellido': form.cleaned_data['apellido'],
                'DPI': form.cleaned_data['DPI'],
                'fecha_nacimiento': form.cleaned_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                'telefono': form.cleaned_data['telefono'],
                'nombre_usuario': form.cleaned_data['nombre_usuario'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'rol_id': 3,  # ID de rol para Estudiante
            }

            endpoint_url = f'{endpoint}/registro_estudiante'
            response = requests.post(endpoint_url, json=datos)

            if response.status_code == 200:
                messages.success(request, 'Usuario registrado exitosamente')
                return redirect('login')
            else:
                error_message = response.json().get('error', 'Ocurrió un error')
                messages.error(request, f"Error: {error_message}")
        else:
            messages.error(request, "Formulario inválido. Verifica los campos.")
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form, **contexto})

def registro_catedratico(request):
    contexto = {'tab': 'Registro de Catedrático'}

    if request.method == 'POST':
        form = RegistroCatedraticoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'registro_catedratico.html', {'form': form, **contexto})

            datos = {
                'nombre': form.cleaned_data['nombre'],
                'apellido': form.cleaned_data['apellido'],
                'DPI': form.cleaned_data['DPI'],
                'password': form.cleaned_data['password'],
                'rol_id': 2,  # ID de rol para Catedrático
            }

            response = requests.post(f'{endpoint}/registro_catedratico', json=datos)

            if response.status_code == 200:
                messages.success(request, 'Catedrático registrado exitosamente')
                return redirect('vista_administrador')
            else:
                error_message = response.json().get('error', 'Ocurrió un error')
                messages.error(request, f"Error: {error_message}")
        else:
            messages.error(request, "Formulario inválido. Verifica los campos.")
    else:
        form = RegistroCatedraticoForm()

    return render(request, 'registro_catedratico.html', {'form': form, **contexto})

def vista_alumno(request):
    contexto = {
        'tab': 'Vista Alumno',
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }
    return render(request, 'alumno.html', contexto)

def vista_catedratico(request):
    contexto = {
        'tab': 'Catedrático',
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }
    return render(request, 'catedratico.html', contexto)

def vista_administrador(request):
    # Obtener listado de usuarios bloqueados
    response = requests.get(f'{endpoint}/listado_usuarios_bloqueados')
    usuarios_bloqueados = response.json() if response.status_code == 200 else []

    contexto = {
        'tab': 'Administración',
        'usuarios_bloqueados': usuarios_bloqueados,
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }

    return render(request, 'admin.html', contexto)

def recuperar_password(request):
    contexto = {'tab': 'Recuperación de Contraseña'}
    
    if request.method == 'POST':
        dato = request.POST.get('dato')

        if not dato:
            messages.error(request, 'Se requiere DPI o email para continuar.')
            return render(request, 'recuperar_password.html', contexto)

        response = requests.post(f'{endpoint}/recuperar_password', json={'DPI': dato})

        if response.status_code == 200:
            messages.success(request, f'Se ha enviado un enlace de recuperación de contraseña a {dato}')
            return redirect('login')

        response = requests.post(f'{endpoint}/recuperar_password', json={'email': dato})

        if response.status_code == 200:
            messages.success(request, f'Se ha enviado un enlace de recuperación de contraseña a {dato}')
            return redirect('login')
        else:
            messages.error(request, response.json().get('error', 'Ocurrió un error al enviar el enlace de recuperación.'))
    
    return render(request, 'recuperar_password.html', contexto)

def restablecer_password(request, token):
    contexto = {'tab': 'Restablecer Contraseña'}
    
    if request.method == 'POST':
        nueva_password = request.POST.get('nueva_password')
        response = requests.post(f'{endpoint}/actualizar_password', json={'token': token, 'nueva_password': nueva_password})
        
        if response.status_code == 200:
            messages.success(request, 'Contraseña restablecida exitosamente.')
            return redirect('login')
        else:
            messages.error(request, 'Error al restablecer la contraseña. Intenta de nuevo.')
    
    return render(request, 'restablecer_password.html', contexto)

def descargar_listado_catedraticos(request):
    return redirect(f"{endpoint}/descargar_catedraticos")

def logout(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

def desbloquear_usuario(request, user_id):
    response = requests.post(f'{endpoint}/desbloquear/{user_id}')

    if response.status_code == 200:
        messages.success(request, f'Usuario con ID {user_id} desbloqueado exitosamente.')
    else:
        messages.error(request, 'Error al desbloquear el usuario. Intenta de nuevo.')
    
    return redirect('vista_administrador')

def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        
        if form.is_valid():
            datos_curso = {
                'nombre': form.cleaned_data['nombre'],
                'codigo': form.cleaned_data['codigo'],
                'costo': float(form.cleaned_data['costo']),
                'horario': form.cleaned_data['horario'],
                'cupo': form.cleaned_data['cupo'],
                'catedratico_id': form.cleaned_data['catedratico_id'],
                'mensaje_bienvenida': form.cleaned_data['mensaje_bienvenida'],
                'estado': form.cleaned_data['estado'],
            }

            # Si el banner fue cargado, lo convertimos a Base64
            banner = form.cleaned_data.get('banner')
            if banner:
                datos_curso['banner'] = base64.b64encode(banner.read()).decode('utf-8')

            # Enviar datos al backend Flask
            response = requests.post(f'{endpoint}/crear_curso', json=datos_curso)

            if response.status_code == 200:
                messages.success(request, 'Curso creado exitosamente.')
                return redirect('vista_administrador')
            else:
                messages.error(request, 'Error al crear el curso. Inténtalo de nuevo.')

        else:
            messages.error(request, 'Formulario inválido. Verifica los campos.')

    else:
        form = CursoForm()

    return render(request, 'crear_curso.html', {'form': form, 'tab': 'Crear Curso'})

def lista_catedraticos(request):
    contexto = {'tab': 'Listado de Catedráticos y Cursos'}
    
    # Hacer una petición GET al backend Flask para obtener la lista de catedráticos y cursos
    response = requests.get(f'{endpoint}/listar_catedraticos_cursos')
    
    if response.status_code == 200:
        catedraticos_cursos = response.json()
        contexto['catedraticos_cursos'] = catedraticos_cursos
        #print(catedraticos_cursos)
    else:
        messages.error(request, 'Error al obtener la lista de catedráticos y cursos.')
        contexto['catedraticos_cursos'] = []

    return render(request, 'listado_catedraticos.html', contexto)