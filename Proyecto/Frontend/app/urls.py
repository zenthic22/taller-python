from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),  # Página de inicio
    path('login/', views.login, name='login'),  # Página de inicio de sesión
    path('registro/', views.registro, name='registro'),  # Página de registro de usuarios
    path('registro_catedratico/', views.registro_catedratico, name='registro_catedratico'),
    path('logout/', views.logout, name='logout'),  # Cerrar sesión
    path('recuperar_password/', views.recuperar_password, name='recuperar_password'),  # Página de recuperación de contraseña
    path('restablecer_password/<str:token>/', views.restablecer_password, name='restablecer_password'),
    path('vista_alumno/', views.vista_alumno, name='vista_alumno'),  # Vista para el alumno
    path('vista_catedratico/', views.vista_catedratico, name='vista_catedratico'),  # Vista para el catedrático
    path('vista_administrador/', views.vista_administrador, name='vista_administrador'),  # Vista para el administrador
    path('desbloquear_usuario/<int:user_id>/', views.desbloquear_usuario, name='desbloquear_usuario'),
    path('descargar_listado_catedraticos/', views.descargar_listado_catedraticos, name='descargar_listado_catedraticos'),
    path('crear_curso/', views.crear_curso, name='crear_curso'),
    path('listar_catedraticos/', views.lista_catedraticos, name='listar_catedraticos'),
    path('editar_banner/<int:curso_id>/', views.editar_banner, name='editar_banner'),
    path('estudiante/inscribir/', views.inscribirse_curso, name='inscribirse_curso'),
    path('estudiante/desinscribir/<int:curso_id>/', views.desinscribirse_curso, name='desinscribirse_curso'),
    path('estudiante/certificado/<int:curso_id>/<int:estudiante_id>/', views.descargar_certificado, name='descargar_certificado'),
    path('ver_cursos_inscritos/', views.ver_cursos_inscritos, name='ver_cursos_inscritos'),  # Añade esta línea
    path('estudiante/completar_curso/<int:curso_id>/', views.completar_curso, name='completar_curso'),
    path('descargar_registro_notas/<int:curso_id>/', views.descargar_registro_notas, name='descargar_registro_notas'),
    path('notas/<int:curso_id>/', views.obtener_notas, name='obtener_notas'),
    path('descargar_notas/<int:curso_id>/', views.descargar_notas, name='descargar_notas'),
]