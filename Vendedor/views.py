from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .forms import VendedorForm
from .models import Vendedor
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class ListaVendedoresView(LoginRequiredMixin,View):
    def get(self, request):
        # Obtener todos los vendedores, ya sean activos o inactivos
        vendedores = Vendedor.objects.all()

        # Número de elementos por página
        elementos_por_pagina = 10  # Puedes ajustar este valor según tus necesidades

        # Crear un objeto Paginator
        paginator = Paginator(vendedores, elementos_por_pagina)

        # Obtener el número de página desde la solicitud GET
        page = request.GET.get('page', 1)

        try:
            # Obtener la página actual
            vendedores = paginator.page(page)
        except PageNotAnInteger:
            # Si la página no es un número entero, mostrar la primera página
            vendedores = paginator.page(1)
        except EmptyPage:
            # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
            vendedores = paginator.page(paginator.num_pages)

        context = {
            'vendedores': vendedores
        }

        return render(request, 'lista_vendedores.html', context)

@login_required
def crear_vendedor(request):
    if request.method == 'POST':
        form = VendedorForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirecciona a una URL donde se muestra el mensaje de éxito, o actualiza la página sin el formulario.
            return render(request, 'vendedor_creado_exito.html', {'message': 'Vendedor Creado con Éxito'})
        else:
            # Si el formulario no es válido, muestra los errores en la misma página.
            return render(request, 'crear_vendedor.html', {'form': form})
    else:
        form = VendedorForm()
        return render(request, 'crear_vendedor.html', {'form': form})

@login_required    
def vendedor_creado_exito(request):
    # No es necesario pasar contexto si solo vas a mostrar un mensaje
    return render(request, 'vendedor_creado_exito.html')
    
    
class EditarVendedorView(View, LoginRequiredMixin):
    def get(self, request, pk):  # Cambiar 'vendedor_id' a 'pk'
        vendedor = get_object_or_404(Vendedor, pk=pk)
        form = VendedorForm(instance=vendedor)
        return render(request, 'editar_vendedor.html', {'form': form, 'vendedor': vendedor})

    def post(self, request, pk):  # Cambiar 'vendedor_id' a 'pk'
        vendedor = get_object_or_404(Vendedor, pk=pk)
        form = VendedorForm(request.POST, instance=vendedor)
        if form.is_valid():
            form.save()
            return redirect('Vendedor:lista_vendedores')
        
        return render(request, 'editar_vendedor.html', {'form': form, 'vendedor': vendedor})
    

@login_required
def editar_vendedores(request, vendedor_id):
    vendedor = get_object_or_404(Vendedor, id=vendedor_id)

    if request.method == 'POST':
        form = VendedorForm(request.POST, instance=vendedor)
        if form.is_valid():
            form.save()
            return render(request, 'vendedor_editado.html', {'success': True, 'message': f'Vendedor Editado satisfactoriamente'})
    else:
        form = VendedorForm(instance=vendedor)

    return render(request, 'editar_vendedor.html', {'form': form, 'vendedor': vendedor})

@login_required
def vendedor_editado_exito(request):
    # No es necesario pasar contexto si solo vas a mostrar un mensaje
    return render(request, 'vendedor_editado.html')


class CambiarEstadoVendedorView(View, LoginRequiredMixin):
    def post(self, request, pk):
        try:
            vendedor = get_object_or_404(Vendedor, pk=pk)
            vendedor.activo = not vendedor.activo
            vendedor.save()
            return JsonResponse({'success': True, 'message': 'El estado del vendedor ha sido cambiado correctamente.'})
        except Exception as e:
            # Manejar cualquier excepción y proporcionar un mensaje de error
            return JsonResponse({'success': False, 'message': f'Error al cambiar el estado del vendedor: {str(e)}'})
        

@login_required
def buscar_vendedor(request):
    search_term = request.GET.get('search', '')
    if search_term:
        vendedores = Vendedor.objects.filter(nombre__icontains=search_term)
    else:
        vendedores = Vendedor.objects.all()

    return render(request, 'lista_vendedores.html', {'vendedores': vendedores})
