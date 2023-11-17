from django.shortcuts import render, redirect, get_object_or_404, redirect
from .forms import ProveedorForm
from .models import Proveedor

def proveedor_create_view(request):
    form = ProveedorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('Proveedor:proveedor-list')

    context = {
        'form': form
    }
    return render(request, "Proveedor/proveedor_form.html", context)

def proveedor_list_view(request):
    proveedores = Proveedor.objects.all()
    context = {
        'proveedores': proveedores
    }
    return render(request, "Proveedor/proveedor_list.html", context)

def proveedor_edit_view(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        return redirect('Proveedor:proveedor-list')
    context = {'form': form}
    return render(request, 'Proveedor/proveedor_edit.html', context)

def proveedor_delete_view(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('Proveedor:proveedor-list')
    context = {'proveedor': proveedor}
    return render(request, 'Proveedor/proveedor_delete.html', context)