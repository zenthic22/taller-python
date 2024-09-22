from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),
]