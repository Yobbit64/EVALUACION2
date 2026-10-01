from django.db import models
from django.contrib.auth.models import User

# Almacena los datos del cliente
# id_cliente es autoincremental y solo puede haber un RUT único por cliente
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)

# Almacena los datos del vehículo
# Relacionado con Cliente (clave foránea)
class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    # Hace que los datos de los objetos en Vehículo aparezcan como texto en la interfaz
    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio}) - RUT Dueño: {self.cliente.rut}"

# Almacena las ventas de un vehículo
# Relacionado con Vehiculo (clave foránea)
class VehiculoVendido(models.Model):
    id_venta = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_venta = models.DateField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    comprador = models.CharField(max_length=150)

# Asocia el user de Django con un RUT único, con tal de poder iniciar sesión con el RUT y la clave del user
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rut = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.rut}"