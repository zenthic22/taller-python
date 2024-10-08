import requests
import base64
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from .forms import RegistroForm, LoginForm, RegistroCatedraticoForm, CursoForm, BannerForm

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
                request.session['usuario_id'] = usuario.get('id')
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
    # Depuración de la sesión
    print("Datos de la sesión:", request.session)

    if not request.session.get('usuario_id'):
        messages.error(request, "Debes iniciar sesión para ver tus cursos.")
        return redirect('login')  # Redirigir a la vista de login

    contexto = {
        'tab': 'Vista Alumno',
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }

    # Petición al endpoint Flask para obtener los cursos disponibles
    response = requests.get(f'{endpoint}/cursos')

    if response.status_code == 200:
        cursos_disponibles = response.json()
        contexto['cursos'] = cursos_disponibles  # Se agrega la lista de cursos al contexto
    else:
        messages.error(request, 'Error al obtener la lista de cursos disponibles.')
        contexto['cursos'] = []  # Si hay un error, se inicializa como lista vacía

    return render(request, 'alumno.html', contexto)

def vista_catedratico(request):
    print(f"Contenido de la sesión: {request.session.items()}")  # Ver el contenido de la sesión

    # Obtener el usuario_id de la sesión
    usuario_id = request.session.get('usuario_id')
    contexto = {
        'tab': 'Catedrático',
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }
    
    print(f"Usuario ID en la sesión (Django): {usuario_id}")  # Verifica el valor del usuario_id en Django
    
    # Petición al endpoint Flask para obtener los cursos
    response = requests.get(f'{endpoint}/profesor/cursos/{usuario_id}')  # Asegúrate de usar el usuario_id correcto

    if response.status_code == 200:
        cursos = response.json()  # Los cursos obtenidos del endpoint Flask
        # Asegúrate de que la respuesta tenga la estructura correcta
        contexto['cursos'] = cursos
    else:
        messages.error(request, 'Error al obtener los cursos asignados.')  # Mensaje de error en caso de fallo
        contexto['cursos'] = []  # Inicializar la lista de cursos vacía

    return render(request, 'catedratico.html', contexto)  # Renderiza la plantilla con el contexto

def vista_administrador(request):
    # Obtener listado de usuarios bloqueados
    response = requests.get(f'{endpoint}/listado_usuarios_bloqueados')
    usuarios_bloqueados = response.json() if response.status_code == 200 else []

    # Obtener listado de cursos
    response_cursos = requests.get(f'{endpoint}/cursos')  # Asegúrate de tener este endpoint configurado
    cursos = response_cursos.json() if response_cursos.status_code == 200 else []

    contexto = {
        'tab': 'Administración',
        'usuarios_bloqueados': usuarios_bloqueados,
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido'),
        'cursos': cursos  # Añadir la lista de cursos al contexto
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

def editar_banner(request, curso_id):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        
        if form.is_valid():
            nuevo_banner = form.cleaned_data['banner']
            
            # Convertir el banner a base64
            banner_b64 = base64.b64encode(nuevo_banner.read()).decode('utf-8')
            
            # Hacer la petición POST a Flask para actualizar el banner
            datos = {
                'curso_id': curso_id,
                'banner': banner_b64
            }

            response = requests.post(f'{endpoint}/profesor/editar_banner', json=datos)
            
            if response.status_code == 200:
                messages.success(request, 'Banner actualizado exitosamente.')
                return redirect('vista_catedratico')
            else:
                messages.error(request, 'Error al actualizar el banner.')
    else:
        form = BannerForm()

    return render(request, 'editar_banner.html', {'form': form, 'curso_id': curso_id})

def inscribirse_curso(request):
    """Permite a los estudiantes inscribirse en un curso."""
    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')  # Obtenemos el curso_id desde el formulario
        estudiante_id = request.session.get('usuario_id')  # Asegúrate de tener esto configurado correctamente

        if curso_id and estudiante_id:
            # Hacer la solicitud al endpoint Flask para inscribirse en el curso
            response = requests.post(f'{endpoint}/estudiante/inscribir', json={'estudiante_id': estudiante_id, 'curso_id': curso_id})

            if response.status_code == 200:
                messages.success(request, 'Te has inscrito correctamente en el curso.')
            else:
                messages.error(request, response.json().get('error', 'Error al inscribirte en el curso.'))
        else:
            messages.error(request, 'El ID del curso y del estudiante son requeridos.')
    
    print(f"Curso ID: {curso_id}, Estudiante ID: {estudiante_id}")
    
    return redirect('vista_alumno')  # Redirige a la vista del alumno después de la inscripción

def desinscribirse_curso(request, curso_id):
    """Permite a los estudiantes desinscribirse de un curso."""
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        messages.error(request, 'Debes iniciar sesión para desinscribirte de un curso.')
        return redirect('login')

    # Enviar la solicitud POST con el curso_id y estudiante_id
    response = requests.post(f'{endpoint}/estudiante/desinscribir', json={'estudiante_id': usuario_id, 'curso_id': curso_id})

    if response.status_code == 200:
        messages.success(request, 'Desinscripción exitosa del curso.')
    else:
        messages.error(request, response.json().get("error", 'Error al desinscribirte del curso.'))

    return redirect('ver_cursos_inscritos')

def descargar_certificado(request, curso_id, estudiante_id):
    """Permite a los estudiantes descargar su certificado si cumplen con los requisitos."""
    if not estudiante_id:
        messages.error(request, 'El ID del estudiante no es válido.')
        return redirect('ver_cursos_inscritos')

    # Hacer la petición para descargar el certificado
    response = requests.get(f'{endpoint}/estudiante/certificado/{curso_id}/{estudiante_id}')

    if response.status_code == 200:
        # Suponiendo que la respuesta es un archivo, puedes manejarlo aquí
        return HttpResponse(response.content, content_type='application/pdf', headers={'Content-Disposition': f'attachment; filename="certificado_curso_{curso_id}.pdf"'})
    else:
        messages.error(request, response.json().get("error", 'Error al descargar el certificado. Verifica tus calificaciones.'))
        return redirect('ver_cursos_inscritos')

def ver_cursos_inscritos(request):
    """Muestra los cursos en los que el estudiante está inscrito."""
    contexto = {
        'tab': 'Cursos Inscritos',
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario desconocido')
    }
    
    estudiante_id = request.session.get('usuario_id')  # Asegúrate de que el ID del estudiante esté almacenado en la sesión
    if not estudiante_id:
        messages.error(request, 'No se encontró el ID del estudiante en la sesión.')
        return render(request, 'cursos_inscritos.html', contexto)

    # Petición al endpoint Flask para obtener los cursos inscritos
    response = requests.get(f'{endpoint}/estudiante/cursos/{estudiante_id}')
    
    # Imprime la respuesta para verificar qué se está recibiendo
    print(response.json())  # Esto te mostrará la respuesta en la consola

    if response.status_code == 200:
        cursos_inscritos = response.json()
        contexto['cursos_inscritos'] = cursos_inscritos  # Se agrega la lista de cursos inscritos al contexto
    else:
        messages.error(request, 'Error al obtener la lista de cursos inscritos.')
        contexto['cursos_inscritos'] = []  # Si hay un error, se inicializa como lista vacía

    return render(request, 'cursos_inscritos.html', contexto)

def completar_curso(request, curso_id):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario_id')

        if not usuario_id:
            messages.error(request, 'Debes iniciar sesión para completar el curso.')
            return redirect('login')

        # Hacer la solicitud al endpoint Flask para completar el curso
        response = requests.post(f'{endpoint}/estudiante/completar_curso/{curso_id}', json={'usuario_id': usuario_id})

        if response.status_code == 200:
            data = response.json()
            messages.success(request, f'Curso completado con nota: {data["nota"]}. {data["mensaje"]}')

            # Verificar si la nota es suficiente para obtener el certificado
            if data["nota"] >= 61:
                return redirect('descargar_certificado', curso_id=curso_id, estudiante_id=usuario_id)  # Redirigir a la vista de descarga del certificado
            else:
                messages.info(request, 'Has completado el curso, pero no alcanzaste la nota mínima para obtener el certificado.')

        else:
            error_message = response.json().get('error', 'Ocurrió un error al completar el curso.')
            messages.error(request, error_message)

    return redirect('vista_alumno')

def descargar_registro_notas(request, curso_id):
    # Hacer una petición GET al backend Flask para descargar el archivo Excel
    response = requests.get(f'{endpoint}/profesor/descargar_registro_notas/{curso_id}', stream=True)

    if response.status_code == 200:
        # Crear un objeto HttpResponse para devolver el archivo Excel
        output = HttpResponse(response.content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        output['Content-Disposition'] = f'attachment; filename=registro_notas_curso_{curso_id}.xlsx'
        return output
    else:
        # Manejar errores de la respuesta
        messages.error(request, 'Error al generar el registro de notas.')
        return HttpResponse("Error al generar el registro de notas.", status=response.status_code)

def obtener_notas(request, curso_id):
    # Petición GET para obtener las notas desde Flask
    try:
        response = requests.get(f"{endpoint}/notas/{curso_id}")
        if response.status_code == 200:
            notas = response.json()  # La lista de notas que devuelve el Flask API
        else:
            notas = []
            print(f"Error al obtener las notas: {response.status_code}")
    except Exception as e:
        print(f"Excepción al obtener las notas: {e}")
        notas = []

    # Si el método es POST, significa que se está editando una nota
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        calificacion = request.POST.get('calificacion')

        # Petición POST para actualizar la nota en Flask (si esta lógica está implementada en Flask)
        try:
            data = {
                'estudiante_id': estudiante_id,
                'calificacion': calificacion
            }
            response = requests.post(f"{endpoint}/notas/{curso_id}", json=data)
            if response.status_code == 200:
                return redirect('obtener_notas', curso_id=curso_id)  # Recargar la página para evitar reenviar el formulario
            else:
                print(f"Error al actualizar la nota: {response.status_code}")
        except Exception as e:
            print(f"Excepción al actualizar la nota: {e}")

    # Renderizar la vista con las notas obtenidas
    return render(request, 'notas.html', {'notas': notas, 'curso_id': curso_id})

def descargar_notas(request, curso_id):
    # Petición GET para descargar el archivo desde Flask
    try:
        # Realizar la solicitud GET a Flask con el curso_id
        response = requests.get(f"{endpoint}/descargar_notas/{curso_id}", stream=True)
        
        # Si la respuesta es exitosa
        if response.status_code == 200:
            # Crear una respuesta HTTP con el contenido del archivo descargado
            response_file = HttpResponse(
                response.content, 
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            # Establecer el encabezado para descargar el archivo como adjunto
            response_file['Content-Disposition'] = f'attachment; filename="notas_curso_{curso_id}.xlsx"'
            return response_file
        else:
            print(f"Error al descargar las notas: {response.status_code}")
            return JsonResponse({'error': 'Error al descargar el archivo'}, status=500)
    
    # Manejo de excepciones en caso de error en la solicitud
    except Exception as e:
        print(f"Excepción al descargar las notas: {e}")
        return JsonResponse({'error': 'No se pudo descargar el archivo'}, status=500)