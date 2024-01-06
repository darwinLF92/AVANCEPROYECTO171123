from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Configuracion
from .forms import ConfiguracionForm
from django.shortcuts import render

class ConfiguracionCreateView(CreateView):
    model = Configuracion
    form_class = ConfiguracionForm
    template_name = 'Configuracion/configuracion_form.html'
    success_url = reverse_lazy('Aplicacion:home')

class ConfiguracionUpdateView(UpdateView):
    model = Configuracion
    form_class = ConfiguracionForm
    template_name = 'Configuracion/configuracion_form.html'
    success_url = reverse_lazy('Aplicacion:home')
    def get_object(self, queryset=None):
        return Configuracion.objects.first()

def mostrar_configuracion(request):
    # Suponiendo que solo hay una configuración en la base de datos.
    configuracion = Configuracion.objects.first()
    return render(request, 'configuracion/mostrar_configuracion.html', {'configuracion': configuracion})
