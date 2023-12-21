from django.db import models
from Clientes.models import Cliente
from Producto.models import Producto
from Vendedor.models import Vendedor
from django.forms import model_to_dict
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import F
from decimal import Decimal
from datetime import timedelta
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction

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
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL , null=True , related_name='vendedor')
    tipo_documento = models.CharField(max_length=7, choices=TIPO_DOCUMENTO_CHOICES)
    tipo_pago = models.CharField(max_length=7, choices=TIPO_PAGO_CHOICES)
    metodo_pago = models.CharField(max_length=8, choices=METODO_PAGO_CHOICES, null=True, blank=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    paga_con = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saldo_pendiente = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    dias_credito = models.IntegerField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    anulada = models.BooleanField(default=False)

    class Meta:
        verbose_name='venta'
        verbose_name_plural = 'ventas'
        order_with_respect_to = 'fecha_creacion'

    def dias_vencidos(self):
        if self.fecha_creacion and self.dias_credito is not None and self.fecha_vencimiento:
            fecha_pago_teorica = self.fecha_creacion + timedelta(days=self.dias_credito)
            fecha_actual = timezone.now().date()  # Usa la fecha actual
            if fecha_pago_teorica < self.fecha_vencimiento:
                # Si la fecha de pago teórica es anterior a la fecha de vencimiento,
                # no hay días vencidos.
                return 0
            return (fecha_actual - fecha_pago_teorica).days - 1
        else:
            return 0 
        
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.pk and self.tipo_pago == 'credito':  
                nuevo_saldo = Decimal(self.cliente.saldo) + Decimal(self.total)
                if nuevo_saldo > self.cliente.limitecredito:
                    raise ValidationError('La venta excede el límite de crédito del cliente.')
            
                self.saldo_pendiente = Decimal(self.total)
                self.cliente.saldo = nuevo_saldo
                self.cliente.save()

            super(Venta, self).save(*args, **kwargs)
    

    

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_compra_en_venta = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
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
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:  # Si es una nueva instancia de DetalleVenta
            if self.producto.stock < self.cantidad:
                raise ValidationError(f'No hay suficiente stock para el producto {self.producto}. Disponible: {self.producto.stock}, Requerido: {self.cantidad}')
        
        self.producto.stock -= self.cantidad  # Reducir el stock
        self.producto.save()
        # Calcula el subtotal teniendo en cuenta el descuento
        self.subtotal = (self.cantidad * self.precio) - self.descuento

        super(DetalleVenta, self).save(*args, **kwargs)


class Cobro(models.Model):
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('cheque', 'Cheque'),
        ('transferencia', 'Transferencia'),
    ]

    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='cobros')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, related_name='cobros')
    fecha_cobro = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=20, decimal_places=2)
    metodo_pago = models.CharField(max_length=13, choices=METODO_PAGO_CHOICES)
    anulado = models.BooleanField(default=False)

    def clean(self):
        if self.monto > self.venta.saldo_pendiente:
            raise ValidationError('El monto del abono no puede superar el saldo pendiente de la venta.')

    def save(self, *args, **kwargs):
        # Bandera para saber si es una nueva instancia o si el monto ha cambiado
        is_new_or_changed = self.pk is None or Cobro.objects.get(pk=self.pk).monto != self.monto

        super().save(*args, **kwargs)

        if is_new_or_changed and not self.anulado:  # Asegurarse de que no esté anulado
            # Actualizar saldos solo si es un nuevo cobro o si el monto ha cambiado
            self.venta.saldo_pendiente -= self.monto
            self.venta.save()
            self.venta.cliente.saldo -= self.monto
            self.venta.cliente.save()
    
    def dif_dias(self):
        if self.fecha_cobro and self.venta.fecha_creacion:
            # Asegúrate de que ambos campos son objetos date; si son DateTimeField, usa .date()
            return (self.fecha_cobro - self.venta.fecha_creacion).days
        else:
            return 0 

    def __str__(self):
        return f'Cobro {self.id} - Venta {self.venta.id}'
    

class Anulacion(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE, related_name='anulacion')
    razon = models.TextField()
    fecha_anulacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anulación de {self.venta}"


class Devolucion(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='devoluciones')
    cantidad = models.PositiveIntegerField()
    razon = models.TextField()
    fecha_devolucion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Devolución {self.id} de Venta {self.venta.id}'
    

class AnulacionCobro(models.Model):
    cobro = models.OneToOneField(Cobro, on_delete=models.CASCADE, related_name='anulacion_cobro')
    fecha_anulacion = models.DateTimeField(auto_now_add=True)
    razon = models.TextField()

    def __str__(self):
        return f'Anulación de Cobro {self.cobro.id} - {self.fecha_anulacion.strftime("%Y-%m-%d")}'
