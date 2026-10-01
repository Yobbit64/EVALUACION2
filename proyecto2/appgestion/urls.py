from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Ruta raíz asociada a la vista index
    path('', views.index, name='index'),
    # Rutas sistema de autenticación de usuario
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
    # Rutas de opciones de gestión
    path('agregar_venta/', views.agregar_venta, name='agregar_venta'),
    path('listar_clientes_vehiculos/', views.listar_clientes_vehiculos, name='listar_clientes_vehiculos'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('listar_ventas/', views.listar_ventas, name='listar_ventas'),
    path('agregar_cliente_vehiculo/', views.agregar_cliente_vehiculo, name='agregar_cliente_vehiculo'),
    path('eliminar_vehiculo/<int:id_vehiculo>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
]