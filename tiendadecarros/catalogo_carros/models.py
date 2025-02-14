from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', default='productos/default-image.jpg')
    destacado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('finalizada', 'Finalizada')
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)  # Fecha de creación
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)  # Fecha de finalización
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Compra {self.id} - {self.cliente.nombre} - {self.estado}"
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Detalle {self.id} - {self.producto.nombre}"
