from django.db import models

class Vendedor(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    fecha_inicio_labores = models.DateField()
    fecha_creacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'vendedor'
        verbose_name_plural = 'vendedores'
        ordering = ['nombre']  # Ordena por nombre de forma ascendente

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
