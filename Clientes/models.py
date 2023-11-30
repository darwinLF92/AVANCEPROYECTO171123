from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nit = models.CharField(max_length=20, verbose_name='NIT')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    direccion = models.CharField(max_length=200, verbose_name='Dirección')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    correo = models.EmailField(max_length=100, verbose_name='Correo Electrónico', blank=True)
    limitecredito = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Límite de Crédito')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return f"{self.nombre} - {self.nit}"

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
