from django.contrib import admin
from .models import Cliente, Vehiculo, VehiculoVendido, Perfil

# Registra el modelo Cliente para su uso en el panel del Administrador
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellidos')
    search_fields = ('rut', 'nombre', 'apellidos')

# Registra el resto de modelos para su uso en el panel de Administrador
admin.site.register(Vehiculo)
admin.site.register(VehiculoVendido)
admin.site.register(Perfil)
