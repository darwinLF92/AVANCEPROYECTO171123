from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Configuracion
from .forms import ConfiguracionForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class ConfiguracionCreateView(LoginRequiredMixin,CreateView):
    model = Configuracion
    form_class = ConfiguracionForm
    template_name = 'Configuracion/configuracion_form.html'
    success_url = reverse_lazy('Aplicacion:home')

class ConfiguracionUpdateView(LoginRequiredMixin,UpdateView):
    model = Configuracion
    form_class = ConfiguracionForm
    template_name = 'Configuracion/configuracion_form.html'
    success_url = reverse_lazy('Aplicacion:home')
    def get_object(self, queryset=None):
        return Configuracion.objects.first()

@login_required
def mostrar_configuracion(request):
    # Suponiendo que solo hay una configuración en la base de datos.
    configuracion = Configuracion.objects.first()
    return render(request, 'configuracion/mostrar_configuracion.html', {'configuracion': configuracion})
