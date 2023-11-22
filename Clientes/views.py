from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente
from Ventas.models import Venta
from django.http import JsonResponse



def cliente_create_view(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Clientes:cliente-list')
    else:
        form = ClienteForm()
    return render(request, 'Clientes/cliente_form.html', {'form': form})

def cliente_list_view(request):
    # Obtener el valor del parámetro de búsqueda "nombre"
    nombre = request.GET.get('nombre', '')

    # Filtrar los clientes por nombre si se proporciona un valor de búsqueda
    if nombre:
        clientes = Cliente.objects.filter(activo=True, nombre__icontains=nombre)
    else:
        # Si no se proporciona un valor de búsqueda, mostrar todos los clientes activos
        clientes = Cliente.objects.filter(activo=True)
    
    return render(request, 'Clientes/cliente_list.html', {'clientes': clientes, 'nombre': nombre})

def cliente_edit_view(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('Clientes:cliente-list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'Clientes/cliente_edit.html', {'form': form})

def cliente_delete_view(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.activo = False  # Cambiar el estado a False en lugar de eliminar
        cliente.save()
        return redirect('Clientes:cliente-list')
    return render(request, 'Clientes/cliente_confirm_delete.html', {'cliente': cliente})


def cliente_search_view(request):
    nombre = request.GET.get('nombre', '')

    if nombre:
        clientes = Cliente.objects.filter(activo=True, nombre__icontains=nombre)
    else:
        clientes = Cliente.objects.filter(activo=True)

    return render(request, 'Clientes/cliente_search_results.html', {'clientes': clientes, 'nombre': nombre})
