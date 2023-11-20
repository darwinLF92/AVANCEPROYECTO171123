from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente
from Ventas.models import Venta

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
    clientes = Cliente.objects.filter(activo=True)
    return render(request, 'Clientes/cliente_list.html', {'clientes': clientes})

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


def detalle_credito_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    ventas_credito = Venta.objects.filter(cliente=cliente, tipo_pago='credito')  # Ajusta este filtro según tu modelo

    return render(request, 'Clientes/detalle_credito_cliente.html', {'cliente': cliente, 'ventas_credito': ventas_credito})