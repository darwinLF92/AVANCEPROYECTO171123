from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import ProveedorForm
from .models import Proveedor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def proveedor_create_view(request):
    form = ProveedorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return render(request, 'Proveedor/proveedor_form.html', {'success': True, 'message': f'Proveedor creado satisfactoriamente'})

    context = {
        'form': form
    }
    return render(request, "Proveedor/proveedor_form.html", context)

def proveedor_list_view(request):
    proveedores = Proveedor.objects.all()

    # Número de elementos por página
    elementos_por_pagina = 10  # Puedes ajustar este valor según tus necesidades

    # Crear un objeto Paginator
    paginator = Paginator(proveedores, elementos_por_pagina)

    # Obtener el número de página desde la solicitud GET
    page = request.GET.get('page', 1)

    try:
        # Obtener la página actual
        proveedores = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        proveedores = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        proveedores = paginator.page(paginator.num_pages)

    context = {
        'proveedores': proveedores
    }

    return render(request, "Proveedor/proveedor_list.html", context)

def proveedor_edit_view(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        return render(request, 'Proveedor/proveedor_form.html', {'success': True, 'message': f'Proveedor editado satisfactoriamente'})
    context = {'form': form}
    return render(request, 'Proveedor/proveedor_edit.html', context)

def proveedor_delete_view(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return render(request, 'Proveedor/proveedor_form.html', {'success': True, 'message': f'Proveedor eliminado satisfactoriamente'})
    context = {'proveedor': proveedor}
    return render(request, 'Proveedor/proveedor_delete.html', context)


def buscar_proveedor3(request):
    search_term = request.GET.get('search', '')
    if search_term:
        proveedores = Proveedor.objects.filter(nombre__icontains=search_term)
    else:
        proveedores = Proveedor.objects.all()

    return render(request, 'Proveedor/proveedor_list.html', {'proveedores': proveedores})