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
    template_name = 'crear_vendedor.html'
    success_template_name = 'create_user.html'

    def get_context_data(self, vendedor=None):
        context = {'form': VendedorForm(instance=vendedor)}
        if vendedor:
            context.update({
                'editando': True,
                'vendedor_nombre': vendedor.nombre,
            })
        else:
            context['editando'] = False
        return context

    def get(self, request, vendedor_id=None):
        vendedor = get_object_or_404(Vendedor, pk=vendedor_id) if vendedor_id else None
        return render(request, self.template_name, self.get_context_data(vendedor))

    def post(self, request, vendedor_id=None):
        vendedor = get_object_or_404(Vendedor, pk=vendedor_id) if vendedor_id else None
        form = VendedorForm(request.POST, instance=vendedor)

        if form.is_valid():
            form.save()
            message = f'Vendedor {vendedor.nombre} creado satisfactoriamente' if vendedor else 'Vendedor creado satisfactoriamente'
            return render(request, self.template_name, {'form': VendedorForm(), 'success': True, 'message': message})
        else:
            return render(request, self.template_name, {'form': form, 'error_message': 'Error en el formulario'})
    
    
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
