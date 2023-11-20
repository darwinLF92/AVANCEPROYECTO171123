from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .forms import VendedorForm
from .models import Vendedor

class ListaVendedoresView(View):
    def get(self, request):
        # Filtrar para obtener solo los vendedores activos
        vendedores_activos = Vendedor.objects.filter(activo=True)
        return render(request, 'lista_vendedores.html', {'vendedores': vendedores_activos})



class CrearVendedorView(View):
    def get(self, request, vendedor_id=None):
        context = {}
        if vendedor_id:
            vendedor = get_object_or_404(Vendedor, pk=vendedor_id)
            form = VendedorForm(instance=vendedor)
            context['editando'] = True
            context['vendedor_nombre'] = vendedor.nombre  # Asegúrate de que el modelo Vendedor tenga el campo 'nombre'
        else:
            form = VendedorForm()
            context['editando'] = False

        context['form'] = form
        return render(request, 'crear_vendedor.html', context)
    
    def post(self, request, vendedor_id=None):
        context = {}
        if vendedor_id:
            vendedor = get_object_or_404(Vendedor, pk=vendedor_id)
            form = VendedorForm(request.POST, instance=vendedor)
            context['editando'] = True
            context['vendedor_nombre'] = vendedor.nombre
        else:
            form = VendedorForm(request.POST)
            context['editando'] = False

        if form.is_valid():
            form.save()
            return redirect('Vendedor:lista_vendedores')

        context['form'] = form
        return render(request, 'crear_vendedor.html', context)
    
    
class EditarVendedorView(View):
    def get(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        form = VendedorForm(instance=vendedor)
        return render(request, 'editar_vendedor.html', {'form': form})

    def post(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        form = VendedorForm(request.POST, instance=vendedor)
        if form.is_valid():
            form.save()
            return redirect('Vendedor:lista_vendedores')
        return render(request, 'editar_vendedor.html', {'form': form})

class CambiarEstadoVendedorView(View):
    def post(self, request, pk):
        vendedor = get_object_or_404(Vendedor, pk=pk)
        vendedor.activo = not vendedor.activo
        vendedor.save()
        return redirect('Vendedor:lista_vendedores')
