from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .forms import VendedorForm
from .models import Vendedor
from django.http import JsonResponse

class ListaVendedoresView(View):
    def get(self, request):
        # Obtener todos los vendedores, ya sean activos o inactivos
        vendedores = Vendedor.objects.all()
        return render(request, 'lista_vendedores.html', {'vendedores': vendedores})



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
        try:
            vendedor = get_object_or_404(Vendedor, pk=pk)
            vendedor.activo = not vendedor.activo
            vendedor.save()
            return JsonResponse({'success': True, 'message': 'El estado del vendedor ha sido cambiado correctamente.'})
        except Exception as e:
            # Manejar cualquier excepción y proporcionar un mensaje de error
            return JsonResponse({'success': False, 'message': f'Error al cambiar el estado del vendedor: {str(e)}'})
