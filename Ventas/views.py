from django.shortcuts import render, redirect
from django.db import transaction
from .forms import VentaForm, DetalleVentaFormSet, DetalleVenta
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, reverse
from .models import Venta, DetalleVenta, Producto, Cliente, Vendedor, Cobro  # Asegúrate de incluir Vendedor aquí
from django.views.generic.edit import FormView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
import json
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
from django.db.models import Sum



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
        action = request.POST.get('action', '')
        if action == 'save':
            try:
                # Crear objeto de Venta
                cliente_id = request.POST.get('cliente')
                cliente = get_object_or_404(Cliente, id=cliente_id)
                vendedor_id = request.POST.get('vendedor')
                vendedor = get_object_or_404(Vendedor, id=vendedor_id)

                venta_data = {
                    'fecha_creacion': request.POST.get('fecha_creacion'),
                    'cliente': cliente,
                    'vendedor': vendedor,
                    'tipo_documento': request.POST.get('tipo_documento'),
                    'tipo_pago': request.POST.get('tipo_pago'),
                    'metodo_pago': request.POST.get('metodo_pago') or None,
                    'total': Decimal(request.POST.get('total')),
                    'paga_con': Decimal(request.POST.get('paga_con')) or None,
                    'cambio': Decimal(request.POST.get('cambio')) or None,
                    'comentarios': request.POST.get('comentarios') or None,
                    'dias_credito': int(request.POST.get('dias_credito')) or None,
                    'fecha_vencimiento': request.POST.get('fecha_vencimiento') or None
                }
                venta = Venta(**venta_data)
                venta.save()

                # Procesar y guardar los detalles de la venta
                verts_items = json.loads(request.POST.get('verts', '[]'))
                for item in verts_items:
                    detalle_data = {
                        'venta': venta,
                        'producto': Producto.objects.get(id=item['id']),
                        'cantidad': int(item['cantidad']),
                        'precio': Decimal(item['precio_venta']),
                        'descuento': Decimal(item['descuento']),
                        'subtotal': Decimal(item['subtotal']),
                        # ... otros campos necesarios ...
                    }
                    try:
                        detalle = DetalleVenta(**detalle_data)
                        detalle.save()
                    except ValidationError as e:
                        data['error'] = str(e)
                        venta.delete()  # Opcional: elimina la venta si no se puede completar
                        break  # Salir del bucle si hay un error

                if 'error' not in data:
                    data['status'] = 'success'
                    data['venta_id'] = venta.id

            except Exception as e:
                data['error'] = 'Error procesando la solicitud: {}'.format(str(e))
        else:
            data['error'] = 'Acción no permitida'

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Productos_list'] = Producto.objects.all()
        context['Clientes_list'] = Cliente.objects.all()
        context['Vendedores_list'] = Vendedor.objects.filter(activo=True)
        return context
    

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

def eliminar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        venta.delete()
        return redirect('Ventas:lista_ventas')  # Redirige a la lista de ventas
    return render(request, 'Ventas/confirmar_eliminar_venta.html', {'venta': venta})

class VentasCreditoPorClienteView(ListView):
    model = Venta
    template_name = 'Ventas/ventas_credito_cliente.html'

    def get_queryset(self):
        # Filtrar solo ventas al crédito
        return Venta.objects.filter(tipo_pago='credito').select_related('cliente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ventas_por_cliente = {}

        for venta in self.object_list:
            # Continuar solo si el saldo pendiente es mayor a cero
            if venta.saldo_pendiente > 0:
                if venta.cliente not in ventas_por_cliente:
                    ventas_por_cliente[venta.cliente] = {
                        'ventas': [],
                        'total_credito': 0
                    }
                
                ventas_por_cliente[venta.cliente]['ventas'].append(venta)
                ventas_por_cliente[venta.cliente]['total_credito'] += venta.saldo_pendiente

        context['ventas_por_cliente'] = ventas_por_cliente
        return context 


class DetalleVentasCreditoClienteView(DetailView):
    model = Cliente
    template_name = 'ventas/lista_creditos.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente_id = self.kwargs.get('pk')

        # Filtrar ventas de crédito con saldo pendiente mayor a cero
        ventas_credito = Venta.objects.filter(cliente_id=cliente_id, tipo_pago='credito', saldo_pendiente__gt=0)

        context['ventas_credito'] = ventas_credito
        return context

    

@csrf_exempt
@require_http_methods(["POST"])
def procesar_cobro(request):
    data = json.loads(request.body)
    cobros = data.get('cobros', [])
    errores = []
    ultimo_cobro_id = None

    for cobro_data in cobros:
        venta_id = cobro_data.get('venta_id')
        monto = Decimal(cobro_data.get('monto'))

        try:
            venta = Venta.objects.get(id=venta_id)
            if monto > venta.saldo_pendiente:
                errores.append(f"El monto del cobro para la venta {venta_id} excede el saldo pendiente.")
                continue

            cobro = Cobro.objects.create(
                venta=venta,
                vendedor=venta.vendedor,
                monto=monto,
                metodo_pago='efectivo'  # O según corresponda
            )
            ultimo_cobro_id = cobro.id
        except Venta.DoesNotExist:
            errores.append(f"Venta con ID {venta_id} no encontrada.")
            continue

    if errores:
        return JsonResponse({"success": False, "errores": errores})
    else:
        # Modifica la siguiente línea para usar una URL válida de recibo
        recibo_url = f"/recibo/{ultimo_cobro_id}/"
        return JsonResponse({"success": True, "recibo_url": recibo_url})

def generar_recibo(request, pk_cobro):
    # Obtener el cobro y la venta asociada
    cobro = get_object_or_404(Cobro, pk=pk_cobro)
    venta = cobro.venta

    # También puedes obtener otros cobros relacionados a la misma venta, si es necesario
    otros_cobros = Cobro.objects.filter(venta=venta).exclude(pk=pk_cobro).select_related('vendedor')

    context = {
        'venta': venta,
        'cobro_actual': cobro,
        'otros_cobros': otros_cobros,
    }

    # Renderizar la plantilla del recibo
    return render(request, 'Ventas/recibo.html', context)

class CobroCreateView(CreateView):
    model = Cobro
    fields = ['venta', 'vendedor', 'monto', 'metodo_pago']
    template_name = 'cobros/cobro_form.html'  # Especifica tu plantilla HTML
    success_url = reverse_lazy('cobros-list')  # URL a redirigir después de un cobro exitoso

    def form_valid(self, form):
        try:
            # Realiza la validación y guarda si es válido
            return super().form_valid(form)
        except ValidationError as e:
            # Agrega el error de validación al formulario y vuelve a mostrar el formulario
            form.add_error(None, e)
            return render(self.request, self.template_name, {'form': form})


class CobrosListView(ListView):
    model = Cobro
    template_name = 'Ventas/cobros_list.html'  # Especifica tu plantilla HTML
    context_object_name = 'cobros'  # Nombre del contexto en la plantilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cobros = Cobro.objects.all()  # Obtén los cobros según tu lógica de filtrado
        total_cobros = cobros.aggregate(total=Sum('monto'))['total']  # Calcula la suma de los montos
        context['cobros'] = cobros
        context['total_cobros'] = total_cobros  # Agrega el total de cobros al contexto
        return context