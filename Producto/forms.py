from django import forms
from .models import Producto, ComponenteProducto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'proveedor', 'descripcion', 'precio_compra', 'precio_venta', 'stock', 'stock_minimo', 'tiene_descuento','es_materia_prima' ,'para_fabricacion']


class ComponenteProductoForm(forms.ModelForm):
    class Meta:
        model = ComponenteProducto
        fields = ['producto_componente', 'cantidad']

    def __init__(self, *args, **kwargs):
        super(ComponenteProductoForm, self).__init__(*args, **kwargs)
        self.fields['producto_componente'].queryset = Producto.objects.filter(activo=True)

    def __init__(self, *args, **kwargs):
        super(ComponenteProductoForm, self).__init__(*args, **kwargs)
        # Asumiendo que existe un atributo en el modelo de 'producto_componente' que marca si es materia prima
        self.fields['producto_componente'].queryset = self.fields['producto_componente'].queryset.filter(es_materia_prima=True)

class ProductoPrincipalForm(forms.Form):
    producto_principal = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True),  # Aquí se filtra por productos activos
        label="Seleccionar Producto Principal",
        empty_label="Seleccione un Producto",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
