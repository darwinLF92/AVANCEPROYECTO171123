from django.db import models

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    proveedor = models.ForeignKey('Proveedor.Proveedor', on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    descripcion = models.TextField(blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=4)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.PositiveIntegerField(default=0, help_text='La cantidad mínima en stock para reorden')
    tiene_descuento = models.BooleanField(default=False)
    es_materia_prima = models.BooleanField(default=False)
    para_fabricacion = models.BooleanField(default=False)
    componentes = models.ManyToManyField('self', through='ComponenteProducto', symmetrical=False, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
    def es_reorden_necesario(self):
        return self.stock <= self.stock_minimo
    
    def actualizar_stock(self, cantidad):
        # Lógica para actualizar el stock
        self.stock -= cantidad
        self.save()

    

class ComponenteProducto(models.Model):
    producto_principal = models.ForeignKey(
        Producto,
        related_name='componentes_principal',  # Cambiado para ser único
        on_delete=models.CASCADE
    )
    producto_componente = models.ForeignKey(
        Producto,
        related_name='componentes_asociados',  # Cambiado para ser único, si es necesario
        on_delete=models.CASCADE
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto_componente.nombre} en {self.producto_principal.nombre}"
    @property
    def costo_total(self):
        return self.cantidad * self.producto_componente.precio_compra
    
    



class Transaccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    # Puedes incluir más campos relevantes aquí, como usuario que realizó la transacción, etc.

    def __str__(self):
        return f"Transacción de {self.cantidad} para {self.producto.nombre} el {self.fecha_registro}"
    

