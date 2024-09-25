import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm, LoginForm, RegistroCatedraticoForm

endpoint = 'http://localhost:3000'

def home(request):
    contexto = {
        'tab': 'Inicio'
    }
    response = requests.get(endpoint)
    return render(request, 'index.html', contexto)

def login(request):
    contexto = {
        'tab': 'Iniciar Sesión',
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }
    
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')  # Cambiado para obtener el nombre de usuario
        dpi = request.POST.get('dpi')
        email = request.POST.get('email')  # Se añadió para el inicio de sesión
        password = request.POST.get('password')

        datos = {
            'nombre_usuario': nombre_usuario,  # Cambiado para incluir el nombre de usuario
            'DPI': dpi,
            'email': email,  # Se añadió para el inicio de sesión
            'password': password,
        }

        response = requests.post(f'{endpoint}/login', json=datos)
        if response.status_code == 200:
            usuario = response.json()
            request.session['nombre_usuario'] = usuario.get('nombre', 'usuario desconocido')
            rol_id = usuario.get('rol_id')
            if rol_id == 1:
                return redirect('vista_administrador')
            elif rol_id == 2:
                return redirect('vista_catedratico')
            elif rol_id == 3:
                return redirect('vista_alumno')
        elif response.status_code == 403:
            messages.error(request, 'Cuenta bloqueada. Contacte al administrador.')
            return redirect('login')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')
    
    return render(request, 'login.html', contexto)

def registro(request):
    contexto = {
        'tab': 'Registro de Usuario'
    }

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            rol_id = int(form.cleaned_data['rol'])  # Convierte a entero
            
            # Verificar el rol y dirigir a la vista adecuada
            if rol_id == 2:  # Catedrático
                return redirect('registro_catedratico')  # Redirige a la vista de registro de catedráticos
            else:
                # Si es otro rol, continua con el registro normal
                # Verificar que las contraseñas coincidan
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
                    'rol_id': rol_id,
                }

                # Determinar el endpoint basado en el rol
                if rol_id == 1:  # Administrador
                    endpoint_url = f'{endpoint}/registro_administrador'
                elif rol_id == 3:  # Estudiante
                    endpoint_url = f'{endpoint}/registro_estudiante'
                else:
                    messages.error(request, "Rol inválido.")
                    return render(request, 'registro.html', {'form': form, **contexto})

                # Realizar la solicitud al endpoint de registro
                response = requests.post(endpoint_url, json=datos)

                if response.status_code == 200:
                    messages.success(request, 'Usuario registrado exitosamente')
                    return redirect('login')
                else:
                    # Manejar el error de respuesta del servidor
                    try:
                        error_message = response.json().get('error', 'Ocurrió un error')
                    except ValueError:
                        error_message = 'No se pudo decodificar la respuesta del servidor.'
                    messages.error(request, f"Error: {error_message}")
        else:
            messages.error(request, "Formulario inválido. Verifica los campos.")
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form, **contexto})

def registro_catedratico(request):
    contexto = {
        'tab': 'Registro de Catedrático'
    }

    if request.method == 'POST':
        form = RegistroCatedraticoForm(request.POST)
        if form.is_valid():
            # Verificar que las contraseñas coincidan
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'registro_catedratico.html', {'form': form, **contexto})

            datos = {
                'nombre': form.cleaned_data['nombre'],
                'apellido': form.cleaned_data['apellido'],
                'DPI': form.cleaned_data['DPI'],
                'password': form.cleaned_data['password'],
                'rol_id': 2,  # ID de rol para Administrador
            }

            # Realizar la solicitud al endpoint de registro
            response = requests.post(f'{endpoint}/registro_catedratico', json=datos)

            if response.status_code == 200:
                messages.success(request, 'Catedrático registrado exitosamente')
                return redirect('vista_administrador')  # Redirige a la vista de administración
            else:
                try:
                    error_message = response.json().get('error', 'Ocurrió un error')
                except ValueError:
                    error_message = 'No se pudo decodificar la respuesta del servidor.'
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
    # Obtén los usuarios bloqueados de tu API
    response = requests.get(f'{endpoint}/listado_usuarios_bloqueados')
    if response.status_code == 200:
        usuarios_bloqueados = response.json()
    else:
        usuarios_bloqueados = []

    contexto = {
        'tab': 'Administracion',
        'usuarios_bloqueados': usuarios_bloqueados,
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }

    return render(request, 'admin.html', contexto)

def recuperar_password(request):
    contexto = {'tab': 'Recuperación de Contraseña'}
    
    if request.method == 'POST':
        dato = request.POST.get('dato')

        # Validar que se haya proporcionado algún dato
        if not dato:
            messages.error(request, 'Se requiere DPI o email para continuar.')
            return render(request, 'recuperar_password.html', contexto)

        # Primero intenta recuperar como DPI
        response = requests.post(f'{endpoint}/recuperar_password', json={'DPI': dato})
        
        if response.status_code == 200:
            messages.success(request, f'Se ha enviado un enlace de recuperación de contraseña a {dato}')
            return redirect('login')
        
        # Si falla, intenta como correo
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
    return redirect(f"{endpoint}/descargar_listado_catedraticos")

def logout(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

def desbloquear_usuario(request, user_id):
    response = requests.post(f'{endpoint}/desbloquear/{user_id}')

    if response.status_code == 200:
        messages.success(request, 'Usuario desbloqueado exitosamente.')
    else:
        messages.error(request, 'Error al desbloquear el usuario. Intente de nuevo.')

    return redirect('vista_administrador')