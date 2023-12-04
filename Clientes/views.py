from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente
from Ventas.models import Venta, DetalleVenta
from django.http import JsonResponse
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
from datetime import datetime




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


def historial_ventas(request):
    cliente_id = request.GET.get('cliente_id')
    cliente = Cliente.objects.get(id=cliente_id) 
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Convertir fechas de string a objeto datetime
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        fecha_inicio = None
        fecha_fin = None

    # Filtrar ventas por cliente, rango de fechas, y solo las activas
    ventas = Venta.objects.filter(cliente_id=cliente_id, anulada=False)
    if fecha_inicio and fecha_fin:
        ventas = ventas.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])

    # Serializar los datos de ventas para la respuesta
    ventas_data = []
    for venta in ventas:
        detalles = DetalleVenta.objects.filter(venta=venta)
        for detalle in detalles:
            precio = (detalle.subtotal / detalle.cantidad)
            ventas_data.append({
                'fecha_venta': venta.fecha_creacion,
                'id_venta': venta.id,
                'comentarios': venta.comentarios,
                'cantidad': detalle.cantidad,
                'producto': detalle.producto.nombre,
                'precio': precio,
                'subtotal': detalle.subtotal
            })

    return JsonResponse({'ventas': ventas_data, 'nombre_cliente': cliente.nombre })
