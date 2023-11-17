from django.shortcuts import render, redirect
from django.db import transaction
from .forms import VentaForm, DetalleVentaFormSet, DetalleVenta
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, redirect, reverse
from .models import Venta, DetalleVenta, Producto, Cliente
from django.views.generic.edit import FormView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
import json
from django.core.exceptions import ValidationError
from decimal import Decimal

@transaction.atomic
def create_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_formset = DetalleVentaFormSet(request.POST)

        if venta_form.is_valid() and detalle_formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.fecha_creacion = timezone.now()  # Asumiendo que quieras capturar este momento
            venta.save()

            for form in detalle_formset:
                if form.is_valid():
                    detalle = form.save(commit=False)
                    detalle.venta = venta
                    detalle.save()

            return redirect('Ventas:lista_ventas')  # Redireccionar a una vista de éxito

    else:
        venta_form = VentaForm()
        detalle_formset = DetalleVentaFormSet(queryset=DetalleVenta.objects.none())

    context = {
        'venta_form': venta_form,
        'detalle_formset': detalle_formset,
    }

    return render(request, 'Ventas/create_venta.html', context)

def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_creacion')
    context = {
        'ventas': ventas,
    }
    return render(request, 'Ventas/lista_ventas.html', context)


from django.shortcuts import render, get_object_or_404

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    context = {
        'venta': venta,
        'detalles': detalles,
    }
    return render(request, 'Ventas/detalle_venta.html', context)



class AddVentaView(ListView):
    model = Venta
    template_name = 'Ventas/crear_venta.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', '')  # Obtener la acción

        if action == 'save':
            try:
            # Procesa los datos del formulario
                cliente_id = request.POST.get('cliente')
                cliente = get_object_or_404(Cliente, id=cliente_id)

                venta_data = {
                'fecha_creacion': request.POST.get('fecha_creacion'),
                'cliente': cliente,
                'tipo_documento': request.POST.get('tipo_documento'),
                'tipo_pago': request.POST.get('tipo_pago'),
                'metodo_pago': request.POST.get('metodo_pago') or None,  # Maneja el campo opcional
                'total': request.POST.get('total'),
                'paga_con': request.POST.get('paga_con') or None,  # Maneja el campo opcional
                'cambio': request.POST.get('cambio') or None,  # Maneja el campo opcional
                'comentarios': request.POST.get('comentarios') or None,  # Maneja el campo opcional
                'dias_credito': request.POST.get('dias_credito') or None,  # Maneja el campo opcional
                'fecha_vencimiento': request.POST.get('fecha_vencimiento') or None,  # Maneja el campo opcional

                }
                venta = Venta(**venta_data)
                venta.save()  # Guarda el objeto de venta

                # Procesar y guardar los detalles de la venta
                verts_items = json.loads(request.POST.get('verts', '[]'))
                for item in verts_items:
                    detalle_data = {
                        'venta': venta,
                        'producto': Producto.objects.get(id=item['id']),
                        'cantidad': item['cantidad'],
                        'precio': Decimal(item['precio_venta']),
                        'descuento': Decimal(item['descuento']),
                        'subtotal': Decimal(item['subtotal']),
                    # ... otros campos necesarios ...
                    }
                    detalle = DetalleVenta(**detalle_data)
                    detalle.save()
                data['status'] = 'success'
            except ValidationError as e:
                data['error'] = str(e)
            except Exception as e:
                data['error'] = 'Error procesando la solicitud: {}'.format(str(e))

        else:
            data['error'] = 'Acción no permitida'

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Productos_list'] = Producto.objects.all()
        context['Clientes_list'] = Cliente.objects.all()
        return context
    

    
@method_decorator(csrf_exempt, name='dispatch')
class VentasView(FormView):
    form_class = VentaForm
    template_name = 'Ventas/crear_venta.html'

    def form_valid(self, form):
        # Este método se llama cuando el formulario es válido
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Esta función define a dónde redirigir al usuario después de un POST exitoso
        return reverse('Ventas:lista_ventas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Productos_list'] = Producto.objects.all()
        context['Clientes_list'] = Cliente.objects.all()
        return context
    
        

class AutocompleteView(View):
    def post(self, request, *args, **kwargs):
        term = request.POST.get('term', '')
        productos = Producto.objects.filter(nombre__icontains=term)[:10]
        data = [{'id': p.id, 'text': p.nombre} for p in productos]
        return JsonResponse(data, safe=False)
    


def create_ventas(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_formset = DetalleVentaFormSet(request.POST)

        if venta_form.is_valid() and detalle_formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.fecha_creacion = timezone.now()
            venta.save()

            for form in detalle_formset:
                detalle = form.save(commit=False)
                detalle.venta = venta
                detalle.save()

            return JsonResponse({'status': 'success', 'redirect_url': reverse('Ventas:lista_ventas')})

        else:
            # Manejar el caso de formularios no válidos
            return JsonResponse({'status': 'error', 'errors': venta_form.errors})

    else:
        venta_form = VentaForm()
        detalle_formset = DetalleVentaFormSet(queryset=DetalleVenta.objects.none())

    productos = Producto.objects.all()
    clientes = Cliente.objects.all()

    context = {
        'venta_form': venta_form,
        'detalle_formset': detalle_formset,
        'productos': productos,
        'clientes': clientes,
    }

    return render(request, 'Ventas/crear_venta.html', context)


def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query)[:10]  # limitamos a 10 resultados
    productos_json = [
        {'id': prod.id, 'nombre': prod.nombre, 'precio': prod.precio_venta, 'stock': prod.stock}
        for prod in productos
    ]
    return JsonResponse(productos_json, safe=False)

def buscar_clientes(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.filter(nombre__icontains=query).values('nit', 'nombre', 'direccion', 'telefono')[:10]  # Limita los resultados
    return JsonResponse(list(clientes), safe=False)
#archivo que contiene ventas