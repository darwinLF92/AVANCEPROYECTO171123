from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nit', 'nombre', 'direccion', 'telefono', 'correo', 'limitecredito']
