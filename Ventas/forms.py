from django import forms
from .models import Venta, DetalleVenta
from django.forms import modelformset_factory
from django.utils import timezone

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = [
            'fecha_creacion','cliente', 'tipo_documento', 'tipo_pago', 'metodo_pago', 
            'total', 'paga_con', 'cambio', 'comentarios', 'dias_credito', 'fecha_vencimiento'
        ]

        # Opcional: Widgets personalizados para ciertos campos
        widgets = {
            'fecha_creacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    # Opcional: Validaciones adicionales
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones personalizadas si lo necesitas


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio', 'descuento', 'subtotal']
        
        # Opcional: Widgets personalizados para ciertos campos
        widgets = {
            'precio': forms.NumberInput(attrs={'step': '0.01'}),
            'descuento': forms.NumberInput(attrs={'step': '0.01'}),
            'subtotal': forms.NumberInput(attrs={'step': '0.01'}),
        }

    # Opcional: Validaciones adicionales
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones personalizadas si lo necesitas

DetalleVentaFormSet = modelformset_factory(
    DetalleVenta,
    form=DetalleVentaForm,
    extra=1,  # Número de formas adicionales que quieras mostrar por defecto
    can_delete=True  # Permite eliminar detalles si es necesario
)
