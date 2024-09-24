import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm, LoginForm, CatedraticoForm

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
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dpi = request.POST.get('dpi')
        password = request.POST.get('password')

        datos = {
            'nombre': nombre,
            'apellido': apellido,
            'DPI': dpi,
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
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'registro.html', {'form': form})

            datos = {
                'nombre': form.cleaned_data['nombre'],
                'apellido': form.cleaned_data['apellido'],
                'DPI': form.cleaned_data['DPI'],
                'fecha_nacimiento': form.cleaned_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                'telefono': form.cleaned_data['telefono'],
                'nombre_usuario': form.cleaned_data['nombre_usuario'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'rol_id': form.cleaned_data['rol'],
            }

            response = requests.post(f'{endpoint}/registro', json=datos)
            if response.status_code == 200:
                messages.success(request, 'Usuario registrado exitosamente')
                return redirect('login')
            else:
                messages.error(request, f"Error: {response.json().get('error', 'Ocurrió un error')}")
        else:
            messages.error(request, "Formulario inválido. Verifica los campos.")
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form, **contexto})

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

    # Imprimir para depuración
    print("Usuarios bloqueados:", usuarios_bloqueados)

    contexto = {
        'tab': 'Administracion',
        'usuarios_bloqueados': usuarios_bloqueados,
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }
    print("Contexto a renderizar:", contexto)

    return render(request, 'admin.html', contexto)


def registrar_catedratico(request):
    contexto = {
        'tab': 'Registro de Catedrático',
    }
    
    if request.method == 'POST':
        form = CatedraticoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'registro_catedratico.html', {'form': form})

            datos = {
                'nombre': form.cleaned_data['nombre'],
                'apellido': form.cleaned_data['apellido'],
                'DPI': form.cleaned_data['DPI'],
                'password': form.cleaned_data['password'],
                'rol_id': 2,
            }

            response = requests.post(f'{endpoint}/registro_catedratico', json=datos)
            if response.status_code == 200:
                messages.success(request, 'Catedrático registrado exitosamente')
                return redirect('vista_administrador')
            else:
                messages.error(request, f"Error: {response.json().get('error', 'Ocurrió un error')}")

    else:
        form = CatedraticoForm()

    return render(request, 'registro_catedratico.html', {'form': form, **contexto})

def recuperar_password(request):
    contexto = {
        'tab': 'Recuperación de Contraseña'
    }
    
    if request.method == 'POST':
        dato = request.POST.get('dato')  # Cambia 'email' a 'dato' para generalizar

        # Intenta recuperar como DPI primero
        response = requests.post(f'{endpoint}/recuperar_password_catedratico', json={'DPI': dato})
        
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
    contexto = {
        'tab': 'Restablecer Contraseña'
    }
    
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