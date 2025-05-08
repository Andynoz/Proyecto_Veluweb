from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('agregar/', views.agregar, name="agregar"),
    path('eliminar/<int:cliente_id>/', views.eliminar, name="eliminar"),
    path('editar/<int:cliente_id>/', views.editar, name="editar"),
    path('clientes/', views.clientes, name="clientes"),
]
