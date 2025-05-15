
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('agregar/', views.agregar, name='agregar'),
    path('editar/<int:cliente_id>/', views.editar, name='editar'),
    path('eliminar/<int:cliente_id>/', views.eliminar, name='eliminar'),
    path('index/', views.index, name='index'),
]
