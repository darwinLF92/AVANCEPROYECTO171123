from django.db import models
from Clientes.models import Cliente
from Producto.models import Producto
from django.forms import model_to_dict
from django.core.exceptions import ValidationError
from django.utils import timezone

class Venta(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('envio', 'Envío'),
        ('factura', 'Factura'),
    ]

    TIPO_PAGO_CHOICES = [
        ('contado', 'Contado'),
        ('credito', 'Crédito'),
    ]

    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('cheque', 'Cheque'),
        ('deposito', 'Depósito'),
    ]

    fecha_creacion = models.DateField(max_length=255)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL , null=True , related_name='clientee')
    tipo_documento = models.CharField(max_length=7, choices=TIPO_DOCUMENTO_CHOICES)
    tipo_pago = models.CharField(max_length=7, choices=TIPO_PAGO_CHOICES)
    metodo_pago = models.CharField(max_length=8, choices=METODO_PAGO_CHOICES, null=True, blank=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    paga_con = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comentarios = models.TextField(blank=True, null=True)
    dias_credito = models.IntegerField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name='venta'
        verbose_name_plural = 'ventas'
        order_with_respect_to = 'fecha_creacion'

    def __str__(self):
        return str(self.id)

    

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    devolucion = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='detalle venta'
        verbose_name_plural = 'detalles venta'
        order_with_respect_to = 'created'

    def __str__(self):
        return self.producto
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['created'])
        return item



