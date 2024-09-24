from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),  # Página de inicio
    path('login/', views.login, name='login'),  # Página de inicio de sesión
    path('registro/', views.registro, name='registro'),  # Página de registro de usuarios
    path('logout/', views.logout, name='logout'),  # Cerrar sesión
    path('recuperar_password/', views.recuperar_password, name='recuperar_password'),  # Página de recuperación de contraseña
    path('restablecer_password/<str:token>/', views.restablecer_password, name='restablecer_password'),
    path('restablecer_password_catedratico/<str:token>/', views.restablecer_password, name='restablecer_password'),
    path('vista_alumno/', views.vista_alumno, name='vista_alumno'),  # Vista para el alumno
    path('vista_catedratico/', views.vista_catedratico, name='vista_catedratico'),  # Vista para el catedrático
    path('vista_administrador/', views.vista_administrador, name='vista_administrador'),  # Vista para el administrador
    path('desbloquear_usuario/<int:user_id>/', views.desbloquear_usuario, name='desbloquear_usuario'),
    path('registrar_catedratico/', views.registrar_catedratico, name='registrar_catedratico'),
    path('descargar_listado_catedraticos/', views.descargar_listado_catedraticos, name='descargar_listado_catedraticos'),
]