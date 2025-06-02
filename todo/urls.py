
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tabla/', views.tabla, name='tabla'),
    path('agregar/', views.agregar, name='agregar'),
    path('editar/<int:cliente_id>/', views.editar, name='editar'),
    path('eliminar/<int:cliente_id>/', views.eliminar, name='eliminar'),
    path('index/', views.index, name='index'),
    path('signIn/', views.signIn, name='signIn'),
    path('logout/', views.signout, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('recuperacion/', views.recuperacion, name='recuperacion'),
    path('recuperar/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('recuperacion/enviado/', views.correo_enviado, name='correo_enviado'),
    path('recuperacion/confirmar/', views.confirmar_contrasena, name='confirmar_contrasena'),
    path('recuperacion/completado/', views.contrasena_cambiada, name='contrasena_cambiada'),
    path('verificar-codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('nueva-contrasena/', views.nueva_contrasena, name='nueva_contrasena'),
    path('bienvenida/', views.bienvenida, name='bienvenida'),
]
