from django.db import models
from django.utils import timezone

class Proveedor(models.Model):
    nit = models.CharField(max_length=20, unique=True, verbose_name='NIT')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    direccion = models.CharField(max_length=200, verbose_name='Dirección')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    correo = models.EmailField(max_length=100, verbose_name='Correo Electrónico')
    contacto = models.CharField(max_length=100, verbose_name='Contacto')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.nombre
    def actualizar_stock(self, cantidad_vendida):
        self.stock -= cantidad_vendida
        self.save()

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']  # Ordena por nombre de forma ascendente


