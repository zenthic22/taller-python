import requests  # Asegúrate de importar requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm, LoginForm

endpoint = 'http://localhost:3000'

def home(request):
    contexto = {
        'tab': 'Inicio'
    }
    response = requests.get(endpoint)
    return render(request, 'index.html', contexto)

# Vista para la página de inicio de sesión
def login(request):
    contexto = {
        'tab': 'Iniciar Sesión'
    }
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            datos = {
                'nombre_usuario': form.cleaned_data['nombre_usuario'],
                'password': form.cleaned_data['password'],
            }
            # Enviar los datos al endpoint Flask
            response = requests.post(f'{endpoint}/login', json=datos)
            if response.status_code == 200:
                messages.success(request, 'Inicio de sesión exitoso')
                return redirect('index')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, **contexto})

# Vista para la página de registro
def registro(request):
    contexto = {
        'tab': 'Registro de Usuario'
    }
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Validar que las contraseñas coincidan
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'registro.html', {'form': form})

            # Extraer los datos del formulario
            datos = {
                'nombre': form.cleaned_data['nombre'],
                'apellido': form.cleaned_data['apellido'],
                'DPI': form.cleaned_data['DPI'],
                'fecha_nacimiento': form.cleaned_data['fecha_nacimiento'].strftime('%Y-%m-%d'),
                'telefono': form.cleaned_data['telefono'],
                'nombre_usuario': form.cleaned_data['nombre_usuario'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'rol_id': form.cleaned_data['rol_id'],
            }
            # Enviar los datos a Flask
            response = requests.post(f'{endpoint}/registro', json=datos)
            if response.status_code == 200:
                messages.success(request, 'Usuario registrado exitosamente')
                return redirect('login')
            else:
                messages.error(request, f"Error: {response.json().get('error', 'Ocurrió un error')}")
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form, **contexto})


def logout(request):
    # Simplemente muestra un mensaje de cierre de sesión
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')