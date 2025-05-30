
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('agregar/', views.agregar, name='agregar'),
    path('editar/<int:cliente_id>/', views.editar, name='editar'),
    path('eliminar/<int:cliente_id>/', views.eliminar, name='eliminar'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('recuperacion/', views.recuperacion, name='recuperacion'),
    path('recuperar/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('recuperar/enviado/', views.correo_enviado, name='correo_enviado'),
    path('recuperar/confirmar/', views.confirmar_contrasena, name='confirmar_contrasena'),
    path('recuperar/completado/', views.contrasena_cambiada, name='contrasena_cambiada'),
    path('verificar-codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('nueva-contrasena/', views.nueva_contrasena, name='nueva_contrasena'),
]
