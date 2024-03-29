from io import BytesIO
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from weasyprint import HTML
from .forms import AnulacionForm, DevolucionForm, VentaForm, DetalleVentaFormSet, DetalleVenta
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, reverse
from .models import Venta, DetalleVenta, Producto, Cliente, Vendedor, Cobro, AnulacionCobro  # Asegúrate de incluir Vendedor aquí
from django.views.generic.edit import FormView
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
import json
from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_http_methods
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from django.db.models import Prefetch, Sum, Case, When, IntegerField
from datetime import timedelta
from django.db.models import ExpressionWrapper, fields
from django.db.models.functions import Now
from django.db.models import Sum, Case, When, Value, IntegerField, F, ExpressionWrapper, fields, Q, DecimalField
from django.db.models.functions import Now, TruncDay, ExtractDay
from django.db.models.functions import Coalesce
from django.template.loader import render_to_string
from datetime import datetime, date
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import tempfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



class ListaVentasView(ListView, LoginRequiredMixin):
    model = Venta
    template_name = 'Ventas/lista_ventas.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        queryset = super().get_queryset().filter(anulada=False)
        cliente_nombre = self.request.GET.get('cliente', '')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        if cliente_nombre:
            queryset = queryset.filter(cliente__nombre__icontains=cliente_nombre)

        if not fecha_inicio or not fecha_fin:
            today = timezone.now().date()
            fecha_inicio = fecha_fin = today

        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])

        # Calcular el total de ventas para el queryset filtrado
        self.total_ventas = queryset.aggregate(totalv=Sum('total'))['totalv'] if queryset.exists() else 0

        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['today'] = today.strftime("%Y-%m-%d")
        context['total_ventas'] = self.total_ventas  # Usar el total calculado en get_queryset
        return context



@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    # Calcular el precio unitario para cada detalle
    for detalle in detalles:
        detalle.precio_unitario = detalle.subtotal / detalle.cantidad if detalle.cantidad else 0

    context = {
        'venta': venta,
        'detalles': detalles,
    }
    return render(request, 'Ventas/detalle_venta.html', context)



class AddVentaView(ListView, LoginRequiredMixin):
    model = Venta
    template_name = 'Ventas/crear_venta.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', '')
        if action == 'save':
            with transaction.atomic():  # Iniciar una transacción
                try:
                    # Obtener datos del formulario
                    cliente_id = request.POST.get('cliente')
                    cliente = get_object_or_404(Cliente, id=cliente_id)
                    vendedor_id = request.POST.get('vendedor')
                    vendedor = get_object_or_404(Vendedor, id=vendedor_id)
                    total_venta = Decimal(request.POST.get('total'))

                    # Verificar límite de crédito del cliente
                    if cliente.saldo + total_venta > cliente.limitecredito:
                        raise ValidationError('La venta excede el límite de crédito del cliente.')

                    # Crear objeto de Venta con datos del formulario
                    venta = Venta(
                        fecha_creacion=request.POST.get('fecha_creacion'),
                        cliente=cliente,
                        vendedor=vendedor,
                        tipo_documento=request.POST.get('tipo_documento'),
                        tipo_pago=request.POST.get('tipo_pago'),
                        metodo_pago=request.POST.get('metodo_pago'),
                        total=total_venta,
                        paga_con=Decimal(request.POST.get('paga_con')),
                        cambio=Decimal(request.POST.get('cambio')),
                        comentarios=request.POST.get('comentarios'),
                        dias_credito=int(request.POST.get('dias_credito')) if request.POST.get('dias_credito') else None,
                        fecha_vencimiento=request.POST.get('fecha_vencimiento'),
                    )
                    venta.save()  # Guardar la venta

                    # Obtener y validar detalles de la venta
                    verts_items = json.loads(request.POST.get('verts', '[]'))
                    for item in verts_items:
                        producto = Producto.objects.get(id=item['id'])
                        cantidad_requerida = int(item['cantidad'])

                        # Validar stock del producto
                        if producto.stock < cantidad_requerida:
                            raise ValidationError(f'No hay suficiente stock para el producto {producto.nombre}. Disponible: {producto.stock}, Requerido: {cantidad_requerida}')

                        # Preparar y guardar los datos del detalle de la venta
                        detalle = DetalleVenta(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad_requerida,
                            precio=Decimal(item['precio_venta']),
                            descuento=Decimal(item['descuento']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                            precio_compra_en_venta=producto.precio_compra,
                            subtotal=Decimal(item['subtotal']),
                            # ... otros campos necesarios ...
                        )
                        detalle.save()

                    data['status'] = 'success'
                    data['venta_id'] = venta.id

                except ValidationError as e:
                    data['error'] = str(e)
                    # En caso de excepción, la transacción se revierte automáticamente

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
    
@login_required
def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query)[:10]  # limitamos a 10 resultados
    productos_json = [
        {'id': prod.id, 'nombre': prod.nombre, 'precio': prod.precio_venta, 'stock': prod.stock}
        for prod in productos
    ]
    return JsonResponse(productos_json, safe=False)

@login_required
def buscar_clientes(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.filter(nombre__icontains=query).values('nit', 'nombre', 'direccion', 'telefono')[:10]  # Limita los resultados
    return JsonResponse(list(clientes), safe=False)
#archivo que contiene ventas
@login_required
def eliminar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'La venta se eliminó correctamente.')  # Agrega un mensaje de éxito
        return redirect('Ventas:eliminacion_exitosa')  # Redirige a la lista de ventas
    return render(request, 'Ventas/confirmar_eliminar_venta.html', {'venta': venta})

@login_required
def venta_eliminada_exito(request):
    # No es necesario pasar contexto si solo vas a mostrar un mensaje
    return render(request, 'Ventas/eliminacion_exitosa.html')



class VentasCreditoPorClienteView(ListView, LoginRequiredMixin):
    model = Venta
    template_name = 'Ventas/ventas_credito_cliente.html'

    def get_queryset(self):
        queryset = Venta.objects.filter(
            tipo_pago='credito',
            saldo_pendiente__gt=0,
            anulada=False
        ).select_related('cliente')

        # Obtener el término de búsqueda del query string
        search_query = self.request.GET.get('filtro_nombre', None)
        if search_query:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=search_query) |
                Q(cliente__apellido__icontains=search_query)
                # Añade aquí otros campos de búsqueda si es necesario
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()  # Asegúrate de usar el queryset filtrado
        ventas_por_cliente = {}

        # Inicializar los totales
        suma_total_documentos = 0
        suma_total_inicial = Decimal('0.00')  # Usar Decimal para evitar problemas de precisión
        suma_abonos = Decimal('0.00')
        suma_saldo_pendiente = Decimal('0.00')

        for venta in queryset:  # Usa el queryset filtrado
            cliente = venta.cliente
            if cliente not in ventas_por_cliente:
                ventas_por_cliente[cliente] = {
                    'cliente': venta.cliente,
                    'ventas': [],
                    'total_inicial': Decimal('0.00'),
                    'total_abonos': Decimal('0.00'),
                    'saldo_pendiente': Decimal('0.00'),
                }

           # Acumular los totales para cada cliente
            ventas_por_cliente[cliente]['ventas'].append(venta)
            ventas_por_cliente[cliente]['total_inicial'] += venta.total
            ventas_por_cliente[cliente]['saldo_pendiente'] += venta.saldo_pendiente

            # Acumular los totales generales
            suma_total_inicial += venta.total
            suma_saldo_pendiente += venta.saldo_pendiente

        # Calcular los abonos para cada cliente y acumular el total de abonos y documentos
        for datos in ventas_por_cliente.values():
            datos['total_abonos'] = datos['total_inicial'] - datos['saldo_pendiente']
            suma_abonos += datos['total_abonos']
            suma_total_documentos += len(datos['ventas'])

        # Agregar los totales acumulados al contexto
        context['ventas_por_cliente'] = ventas_por_cliente
        context['suma_total_documentos'] = suma_total_documentos
        context['suma_total_inicial'] = suma_total_inicial
        context['suma_abonos'] = suma_abonos
        context['suma_saldo_pendiente'] = suma_saldo_pendiente

        return context
    
class DetalleVentasCreditoClienteView(DetailView, LoginRequiredMixin):
    model = Cliente
    template_name = 'ventas/lista_creditos.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente_id = self.kwargs.get('pk')

        # Filtrar ventas de crédito con saldo pendiente mayor a cero
        ventas_credito = Venta.objects.filter(cliente_id=cliente_id, 
        tipo_pago='credito', saldo_pendiente__gt=0, anulada=False).order_by('-id')

        context['ventas_credito'] = ventas_credito
        return context

    

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def procesar_cobro(request):
    data = json.loads(request.body)
    cobros = data.get('cobros', [])
    errores = []
    cliente_id = None

    for cobro_data in cobros:
        venta_id = cobro_data.get('venta_id')
        monto = Decimal(cobro_data.get('monto')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        metodo_pago = cobro_data.get('metodo_pago')

        try:
            venta = Venta.objects.get(id=venta_id)
            cliente_id = venta.cliente.id  # Asumiendo que Venta tiene una relación con Cliente

            if monto > venta.saldo_pendiente:
                errores.append(f"El monto del cobro para la venta {venta_id} excede el saldo pendiente.")
                continue

            cobro = Cobro.objects.create(
                venta=venta,
                vendedor=venta.vendedor,
                monto=monto,
                metodo_pago=metodo_pago
            )
        except Venta.DoesNotExist:
            errores.append(f"Venta con ID {venta_id} no encontrada.")
            continue

    if errores:
        return JsonResponse({"success": False, "errores": errores})
    else:
        # Construye la URL para redirigir a la lista de créditos del cliente
        lista_creditos_url = reverse('Ventas:lista_creditos', args=[cliente_id])
        return JsonResponse({"success": True, "lista_creditos_url": lista_creditos_url})


@login_required
def generar_recibo(request, pk_cobro):
    cobro = get_object_or_404(Cobro, pk=pk_cobro)
    venta = cobro.venta
    detalles_venta = venta.detalles.all()

    otros_cobros = Cobro.objects.filter(venta=venta).exclude(pk=pk_cobro).select_related('vendedor')

    total_abonado = otros_cobros.aggregate(Sum('monto'))['monto__sum'] or 0

    context = {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'cobro_actual': cobro,
        'otros_cobros': otros_cobros,
        'total_abonado': total_abonado,
    }

    return render(request, 'Ventas/recibo.html', context)


class CobroCreateView(CreateView, LoginRequiredMixin):
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


class CobrosListView(ListView, LoginRequiredMixin):
    model = Cobro
    template_name = 'Ventas/cobros_list.html'
    context_object_name = 'cobros'

    def get_queryset(self):
        queryset = super().get_queryset().filter(anulado=False) 
        cliente_nombre = self.request.GET.get('cliente', '')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        if cliente_nombre:
            queryset = queryset.filter(venta__cliente__nombre__icontains=cliente_nombre)
        # Si no se proporcionan fechas, se filtra por el día actual
        if not fecha_inicio or not fecha_fin:
            today = timezone.now().date()
            fecha_inicio = fecha_fin = today

        if fecha_inicio and fecha_fin:
            # Filtrar cobros por el rango de fechas
            queryset = queryset.filter(fecha_cobro__range=[fecha_inicio, fecha_fin])

        return queryset.order_by('-id') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['today'] = today.strftime("%Y-%m-%d")  # Formato de fecha 'YYYY-MM-DD'

        # Calcular el total de cobros
        cobros = self.get_queryset()
        total_cobros = cobros.aggregate(total=Sum('monto'))['total'] if cobros else 0
        context['total_cobros'] = total_cobros
        return context
    
from reportlab.lib.pagesizes import letter

def format_currency(value):
    return "{:,.2f}".format(value)

@login_required
def imprimir_venta(request, venta_id):
    venta = Venta.objects.get(pk=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Venta-{venta.id}-{venta.cliente.nombre}-{venta.fecha_creacion.strftime("%d-%m-%Y")}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Tamaño de la hoja (carta)
    
    # Organizar el contenido
    p.drawString(85, height - 117, f"{venta.cliente.nombre}")
    p.drawString(95, height - 133, f"{venta.cliente.direccion}")
    p.drawString(500, height - 133, f"{venta.cliente.telefono}")
    
    fecha = venta.fecha_creacion.strftime('%d %m %Y').split(' ')
# Asumiendo que tienes una diferencia de 20 puntos entre cada parte de la fecha
    p.drawString(465, height - 95, fecha[0])  # Día
    p.drawString(500, height - 95, fecha[1])  # Mes
    p.drawString(535, height - 95, fecha[2])  # Año

    p.drawString(150, height - 100, f"{venta.id}")
    
    y_position = height - 183
    for detalle in detalles:
        precio_con_descuento = detalle.subtotal / detalle.cantidad if detalle.cantidad else 0
        p.drawString(50, y_position, format_currency(detalle.cantidad))
        p.drawString(95, y_position, f"{detalle.producto.nombre}")
        p.drawString(462, y_position, format_currency(precio_con_descuento))              
        p.drawString(520, y_position, format_currency(detalle.subtotal))
        y_position -= 18
    
    p.drawString(50, 98, f"{venta.comentarios}")
    
    # Totales y pie de página
    p.drawString(520, 110, format_currency(venta.total))
    
    p.showPage()
    p.save()
    
    return response

# views.py
@login_required
def anular_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    if request.method == 'POST':
        form = AnulacionForm(request.POST)
        if form.is_valid():
            anulacion = form.save(commit=False)
            anulacion.venta = venta
            anulacion.save()
            # Actualizar el inventario y el saldo del cliente
            for detalle in venta.detalles.all():
                detalle.producto.stock += detalle.cantidad
                detalle.producto.save()
            if venta.tipo_pago == 'credito':
                venta.cliente.saldo -= venta.total
                venta.cliente.save()
            # Marcar la venta como anulada
            venta.anulada = True
            venta.save()
            return redirect('Ventas:anulacion_exitosa')
    else:
        form = AnulacionForm()

    return render(request, 'Ventas/anular_venta.html', {'venta': venta, 'form': form})

@login_required
def venta_anulada_exito(request):
    # No es necesario pasar contexto si solo vas a mostrar un mensaje
    return render(request, 'Ventas/anulacion_exitosa.html')

#reporte de cuentas por cobrar
@login_required
def reporte_cuentasxcobrar(request):
    fecha_hoy = timezone.now().date()
    clientes_data = []
    vendedores = Vendedor.objects.filter(activo=True).values_list('nombre', flat=True)
    resumen_data = {
        'total_facturado': 0,
        'total_cobrar': 0,
        'total_sin_vencer': 0,
        'total_1_30_dias': 0,
        'total_31_60_dias': 0,
        'total_61_90_dias': 0,
        'total_91_120_dias': 0,
        'total_mas_121_dias': 0,
    }

    # Capturar los parámetros de filtrado
    filtro_cliente = request.GET.get('cliente')
    filtro_vendedor = request.GET.get('vendedor')

    # Filtrar clientes según los parámetros
    clientes_queryset = Cliente.objects.annotate(
        total_saldo_pendiente=Sum('clientee__saldo_pendiente')
    ).filter(total_saldo_pendiente__gt=0)

    if filtro_cliente:
        clientes_queryset = clientes_queryset.filter(nombre__icontains=filtro_cliente)
    
    # Asegúrate de tener una lista de todos los clientes primero antes de filtrar las ventas
    clientes = list(clientes_queryset)
    
    # Si se ha proporcionado un filtro de vendedor, obtener las ventas filtradas por vendedor
    if filtro_vendedor:
        ventas_vendedor = Venta.objects.filter(vendedor__nombre__icontains=filtro_vendedor, saldo_pendiente__gt=0, anulada=False, tipo_pago='credito')
        # Filtrar la lista de clientes basada en las ventas del vendedor
        clientes = [cliente for cliente in clientes if cliente.clientee.filter(id__in=ventas_vendedor).exists()]

    for cliente in clientes:
        cliente.ventas_credito = cliente.clientee.filter(tipo_pago='credito', saldo_pendiente__gt=0, anulada=False).order_by('-id')
        cliente.total_monto = 0
        cliente.total_cobrar = 0
        cliente.total_sin_vencer = 0
        cliente.total_1_30 = 0
        cliente.total_31_60 = 0
        cliente.total_61_90 = 0
        cliente.total_91_120 = 0
        cliente.total_121_mas = 0

        ventas_credito_data = []
        for venta in cliente.ventas_credito:
            dias_vencidos = venta.dias_vencidos()
            venta.total_dias = venta.dias_vencidos() + venta.dias_credito
            cliente.total_monto += venta.total
            cliente.total_cobrar += venta.saldo_pendiente

            if dias_vencidos <= 0:
                cliente.total_sin_vencer += venta.saldo_pendiente
            elif 1 <= dias_vencidos <= 60:
                cliente.total_1_30 += venta.saldo_pendiente
            elif 61 <= dias_vencidos <= 90:
                cliente.total_61_90 += venta.saldo_pendiente
            elif 91 <= dias_vencidos <= 120:
                cliente.total_91_120 += venta.saldo_pendiente
            elif dias_vencidos > 120:
                cliente.total_121_mas += venta.saldo_pendiente


            ventas_credito_data.append({
                'id': venta.id,
                'comentarios': venta.comentarios,
                'fecha_creacion': venta.fecha_creacion,
                'fecha_vencimiento': venta.fecha_vencimiento,
                'dias_vencidos': venta.dias_vencidos(),
                'total': venta.total,
                'saldo_pendiente': venta.saldo_pendiente,
                'total_dias': venta.total_dias,
            })

        clientes_data.append({
            'nombre': cliente.nombre,
            'ventas_credito': ventas_credito_data,
            'total_monto': cliente.total_monto,
            'total_cobrar': cliente.total_cobrar,
            'total_sin_vencer': cliente.total_sin_vencer,
            'total_1_30': cliente.total_1_30,
            'total_61_90': cliente.total_61_90,
            'total_91_120': cliente.total_91_120,
            'total_121_mas': cliente.total_121_mas,
            
        })

        resumen_data['total_facturado'] += cliente.total_monto
        resumen_data['total_cobrar'] += cliente.total_cobrar
        resumen_data['total_sin_vencer'] += cliente.total_sin_vencer
        resumen_data['total_1_30_dias'] += cliente.total_1_30
        resumen_data['total_61_90_dias'] += cliente.total_61_90
        resumen_data['total_91_120_dias'] += cliente.total_91_120
        resumen_data['total_mas_121_dias'] += cliente.total_121_mas


    # Preparar la respuesta con los datos de los clientes y el resumen
    response_data = {
        'clientes': clientes_data,
        'fecha_hoy': fecha_hoy.isoformat(),
        'resumen': resumen_data,
        'vendedores': list(vendedores)  # Convertir a lista si no lo es ya
    }

    return JsonResponse(response_data)

@login_required
def reporte_cuentasxcobrar_pdf(request):
    fecha_hoy = timezone.now().date()
    clientes_data = []
    vendedores = Vendedor.objects.filter(activo=True).values_list('nombre', flat=True)
    resumen_data = {
        'total_facturado': 0,
        'total_cobrar': 0,
        'total_sin_vencer': 0,
        'total_1_30_dias': 0,
        'total_31_60_dias': 0,
        'total_61_90_dias': 0,
        'total_91_120_dias': 0,
        'total_mas_121_dias': 0,
    }

    # Capturar los parámetros de filtrado
    filtro_cliente = request.GET.get('cliente')
    filtro_vendedor = request.GET.get('vendedor')

    # Filtrar clientes según los parámetros
    clientes_queryset = Cliente.objects.annotate(
        total_saldo_pendiente=Sum('clientee__saldo_pendiente')
    ).filter(total_saldo_pendiente__gt=0)

    if filtro_cliente:
        clientes_queryset = clientes_queryset.filter(nombre__icontains=filtro_cliente)
    
    # Asegúrate de tener una lista de todos los clientes primero antes de filtrar las ventas
    clientes = list(clientes_queryset)
    
    # Si se ha proporcionado un filtro de vendedor, obtener las ventas filtradas por vendedor
    if filtro_vendedor:
        ventas_vendedor = Venta.objects.filter(vendedor__nombre__icontains=filtro_vendedor, saldo_pendiente__gt=0, anulada=False, tipo_pago='credito')
        # Filtrar la lista de clientes basada en las ventas del vendedor
        clientes = [cliente for cliente in clientes if cliente.clientee.filter(id__in=ventas_vendedor).exists()]

    for cliente in clientes:
        cliente.ventas_credito = cliente.clientee.filter(tipo_pago='credito', saldo_pendiente__gt=0, anulada=False).order_by('-id')
        cliente.total_monto = 0
        cliente.total_cobrar = 0
        cliente.total_sin_vencer = 0
        cliente.total_1_30 = 0
        cliente.total_31_60 = 0
        cliente.total_61_90 = 0
        cliente.total_91_120 = 0
        cliente.total_121_mas = 0

        ventas_credito_data = []
        for venta in cliente.ventas_credito:
            dias_vencidos = venta.dias_vencidos()
            venta.total_dias = venta.dias_vencidos() + venta.dias_credito
            cliente.total_monto += venta.total
            cliente.total_cobrar += venta.saldo_pendiente

            if dias_vencidos <= 0:
                cliente.total_sin_vencer += venta.saldo_pendiente
            elif 1 <= dias_vencidos <= 60:
                cliente.total_1_30 += venta.saldo_pendiente
            elif 61 <= dias_vencidos <= 90:
                cliente.total_61_90 += venta.saldo_pendiente
            elif 91 <= dias_vencidos <= 120:
                cliente.total_91_120 += venta.saldo_pendiente
            elif dias_vencidos > 120:
                cliente.total_121_mas += venta.saldo_pendiente


            ventas_credito_data.append({
                'id': venta.id,
                'comentarios': venta.comentarios,
                'fecha_creacion': venta.fecha_creacion,
                'fecha_vencimiento': venta.fecha_vencimiento,
                'dias_vencidos': venta.dias_vencidos(),
                'total': venta.total,
                'saldo_pendiente': venta.saldo_pendiente,
                'total_dias': venta.total_dias,
            })

        clientes_data.append({
            'nombre': cliente.nombre,
            'ventas_credito': ventas_credito_data,
            'total_monto': cliente.total_monto,
            'total_cobrar': cliente.total_cobrar,
            'total_sin_vencer': cliente.total_sin_vencer,
            'total_1_30': cliente.total_1_30,
            'total_61_90': cliente.total_61_90,
            'total_91_120': cliente.total_91_120,
            'total_121_mas': cliente.total_121_mas,
            
        })

        resumen_data['total_facturado'] += cliente.total_monto
        resumen_data['total_cobrar'] += cliente.total_cobrar
        resumen_data['total_sin_vencer'] += cliente.total_sin_vencer
        resumen_data['total_1_30_dias'] += cliente.total_1_30
        resumen_data['total_61_90_dias'] += cliente.total_61_90
        resumen_data['total_91_120_dias'] += cliente.total_91_120
        resumen_data['total_mas_121_dias'] += cliente.total_121_mas

    data = {
        'clientes': clientes_data,
        'fecha_hoy': fecha_hoy,
        'resumen': resumen_data,
        'vendedores': list(vendedores),
        'filtro_cliente': filtro_cliente,
        'filtro_vendedor': filtro_vendedor,
    }

    # Renderiza la plantilla HTML con los datos
    html_string = render_to_string('Ventas/reporte_CXC.html', data)

    # Crea un objeto HTML de WeasyPrint
    html = HTML(string=html_string)

    # Configura la respuesta HTTP con el tipo MIME correcto para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Estado_Cuenta.pdf"'

    # Genera el PDF y lo retorna en la respuesta
    html.write_pdf(response)

    return response

from django.core.exceptions import ObjectDoesNotExist

@login_required
def reporte_cobros(request):
    vendedores = list(Vendedor.objects.filter(activo=True).values_list('nombre', flat=True))
    filtro_cliente = request.GET.get('cliente', '')
    filtro_vendedor = request.GET.get('vendedor', '')
    fecha_inicio_str = request.GET.get('fechainicio', '')
    fecha_fin_str = request.GET.get('fechafin', '')
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')

    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None

    # Incluir solo los cobros que no están anulados
    cobros_qs = Cobro.objects.filter(anulado=False)

    if filtro_cliente:
        cobros_qs = cobros_qs.filter(venta__cliente__nombre__icontains=filtro_cliente)
    if filtro_vendedor:
        cobros_qs = cobros_qs.filter(vendedor__nombre__icontains=filtro_vendedor)
    if fecha_inicio:
        cobros_qs = cobros_qs.filter(fecha_cobro__gte=fecha_inicio)
    if fecha_fin:
        cobros_qs = cobros_qs.filter(fecha_cobro__lte=fecha_fin)

    cobros_data = []
    for cobro in cobros_qs:
        try:
            cobros_data.append({
                "cobro_id": cobro.id,
                "venta_id": cobro.venta.id,
                "fecha_creacion": cobro.venta.fecha_creacion.strftime('%Y-%m-%d'),
                "fecha_cobro": cobro.fecha_cobro.strftime('%Y-%m-%d'),
                "dif_dias": cobro.dif_dias(),
                "cliente": cobro.venta.cliente.nombre,
                "comentarios": cobro.venta.comentarios,
                "monto": cobro.monto
            })
        except ObjectDoesNotExist:
            continue  # Omitir la iteración actual si no existen objetos relacionados

    monto_total = cobros_qs.aggregate(Sum('monto'))['monto__sum'] or 0

    return JsonResponse({
        'cobros': cobros_data,
        'monto_total': monto_total,
        'fecha_hoy': fecha_hoy,
        'vendedores': vendedores
    })

@login_required
def reporte_cobros_pdf(request):
    # Obtener lista de vendedores activos
    vendedores = list(Vendedor.objects.filter(activo=True).values_list('nombre', flat=True))

    # Obtener filtros desde la solicitud
    filtro_cliente = request.GET.get('cliente', '')
    filtro_vendedor = request.GET.get('vendedor', '')
    fecha_inicio_str = request.GET.get('fechainicio', '') or datetime.now().strftime('%Y-%m-%d')
    fecha_fin_str = request.GET.get('fechafin', '') or datetime.now().strftime('%Y-%m-%d')

    # Convertir cadenas de fecha a objetos de fecha, si se proporcionan
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None

    # Filtrar los cobros según los criterios proporcionados
    cobros_qs = Cobro.objects.filter(anulado=False)
    if filtro_cliente:
        cobros_qs = cobros_qs.filter(venta__cliente__nombre__icontains=filtro_cliente)
    if filtro_vendedor:
        cobros_qs = cobros_qs.filter(vendedor__nombre__icontains=filtro_vendedor)
    if fecha_inicio:
        cobros_qs = cobros_qs.filter(fecha_cobro__gte=fecha_inicio)
    if fecha_fin:
        cobros_qs = cobros_qs.filter(fecha_cobro__lte=fecha_fin)

    # Preparar los datos para la plantilla
    cobros_data = []
    for cobro in cobros_qs:
        try:
            cobros_data.append({
                "cobro_id": cobro.id,
                "venta_id": cobro.venta.id,
                "fecha_creacion": cobro.venta.fecha_creacion.strftime('%Y-%m-%d'),
                "fecha_cobro": cobro.fecha_cobro.strftime('%Y-%m-%d'),
                "dif_dias": cobro.dif_dias(),  # Asegúrate de que este método existe en tu modelo
                "cliente": cobro.venta.cliente.nombre,
                "comentarios": cobro.venta.comentarios,
                "monto": cobro.monto
            })
        except ObjectDoesNotExist:
            continue  # Omitir la iteración actual si no existen objetos relacionados

    # Calcular el monto total
    monto_total = cobros_qs.aggregate(Sum('monto'))['monto__sum'] or 0

    # Renderizar la plantilla HTML con los datos
    html_string = render_to_string('Ventas/reporte_cobros.html', {
        'datos': cobros_data,
        'monto_total': monto_total,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
        'filtro_cliente': filtro_cliente,
        'filtro_vendedor': filtro_vendedor,
    })

    # Crear un PDF usando WeasyPrint
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Crear una respuesta HTTP con el PDF
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_cobros.pdf"'

    return response

@login_required
def anular_cobro(request, cobro_id):
    cobro = get_object_or_404(Cobro, pk=cobro_id)

    if request.method == 'POST':
        razon_anulacion = request.POST.get('razon_anulacion')

        try:
            with transaction.atomic():
                # Obtener la venta y el cliente asociados al cobro
                venta = cobro.venta
                cliente = venta.cliente

                print("Saldo del cliente antes de anular: ", cliente.saldo)
                print("Saldo pendiente de la venta antes de anular: ", venta.saldo_pendiente)

                cliente.saldo += cobro.monto
                cliente.save()

                venta.saldo_pendiente += cobro.monto
                venta.save()

                print("Saldo del cliente después de anular: ", cliente.saldo)
                print("Saldo pendiente de la venta después de anular: ", venta.saldo_pendiente)

                # Marcar el cobro como anulado
                cobro.anulado = True
                cobro.save()

                AnulacionCobro.objects.create(
                    cobro=cobro,
                    fecha_anulacion=timezone.now(),
                    razon=razon_anulacion
                )

            messages.success(request, 'Cobro anulado con éxito.')
            return redirect('Ventas:cobros-list')  # Reemplaza con la URL de destino adecuada

        except Exception as e:
            messages.error(request, f'Ocurrió un error al anular el cobro: {e}')
            # Considera agregar registros en lugar de imprimir en un entorno de producción

    context = {'cobro': cobro}
    return render(request, 'ventas/anular_cobro.html', context)


@login_required
def reporte_ventas(request):

    vendedores = list(Vendedor.objects.filter(activo=True).values_list('nombre', flat=True))
    filtro_cliente = request.GET.get('cliente', '')
    filtro_producto = request.GET.get('productos', '')
    filtro_vendedor = request.GET.get('vendedor', '')
    fecha_inicio_str = request.GET.get('fechainiciov', '')
    fecha_fin_str = request.GET.get('fechafinv', '')
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')

    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None

    # Incluir solo los cobros que no están anulados
    ventas_qs = Venta.objects.filter(anulada=False)

    if filtro_cliente:
        ventas_qs = ventas_qs.filter(cliente__nombre__icontains=filtro_cliente)
    if filtro_vendedor:
        ventas_qs = ventas_qs.filter(vendedor__nombre__icontains=filtro_vendedor)
    if fecha_inicio:
        ventas_qs = ventas_qs.filter(fecha_creacion__gte=fecha_inicio)
    if fecha_fin:
        ventas_qs = ventas_qs.filter(fecha_creacion__lte=fecha_fin)
        
     # Preparar la consulta inicial para DetalleVenta
    detalles_qs = DetalleVenta.objects.filter(venta__in=ventas_qs)

    # Aplicar filtro de producto en DetalleVenta
    if filtro_producto:
        detalles_qs = detalles_qs.filter(producto__nombre__icontains=filtro_producto)

     # Agregando a nivel de producto
    datos_agrupados = detalles_qs.values(
        'producto_id', 'producto__nombre'
    ).annotate(
        cantidad_total=Sum('cantidad'),
        costo_total=Sum(F('cantidad') * F('precio_compra_en_venta')),
        ventas_total=Sum((F('cantidad') * F('precio')) - F('descuento')),
        renta_bruta=ExpressionWrapper(F('ventas_total') - F('costo_total'), output_field=DecimalField()),
        porcentaje_renta=ExpressionWrapper(F('renta_bruta') / F('ventas_total') * 100, output_field=DecimalField())
    )

    datos_ventas = [
        {
            'producto_id': dato['producto_id'],
            'nombre_producto': dato['producto__nombre'],
            'cantidad': dato['cantidad_total'],
            'costo_total': dato['costo_total'],
            'ventas_total': dato['ventas_total'],
            'renta_bruta': dato['renta_bruta'],
            'porcentaje_renta': dato['porcentaje_renta'],
            
        }
        for dato in datos_agrupados
    ]

    # Cálculos de totales
    total_cant = sum(item['cantidad'] for item in datos_ventas)
    total_costos = sum(item['costo_total'] for item in datos_ventas)
    total_ventas = sum(item['ventas_total'] for item in datos_ventas)
    total_renta = sum(item['renta_bruta'] for item in datos_ventas)
    porcentaje_total = (total_ventas - total_costos) / total_ventas * 100 if total_ventas else 0

    return JsonResponse({
        'ventas': datos_ventas,
        'total_cant': total_cant,
        'total_costos': total_costos,
        'total_ventas': total_ventas,
        'total_renta': total_renta,
        'porcentaje_total': porcentaje_total,
        'fecha_hoy': fecha_hoy,
        'vendedores': vendedores
    })


@login_required
def reporte_ventas_pdf(request):
    # Obtener lista de vendedores activos
    vendedores = list(Vendedor.objects.filter(activo=True).values_list('nombre', flat=True))
    filtro_cliente = request.GET.get('cliente', '')
    filtro_producto = request.GET.get('productos', '')
    filtro_vendedor = request.GET.get('vendedor', '')
    fecha_inicio_str = request.GET.get('fechainiciov', '') or datetime.now().strftime('%Y-%m-%d')
    fecha_fin_str = request.GET.get('fechafinv', '') or datetime.now().strftime('%Y-%m-%d')
   
    # Convertir cadenas de fecha a objetos de fecha, si se proporcionan
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else None
    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else None

    # Incluir solo los cobros que no están anulados
    ventas_qs = Venta.objects.filter(anulada=False)

    if filtro_cliente:
        ventas_qs = ventas_qs.filter(cliente__nombre__icontains=filtro_cliente)
    if filtro_vendedor:
        ventas_qs = ventas_qs.filter(vendedor__nombre__icontains=filtro_vendedor)
    if fecha_inicio:
        ventas_qs = ventas_qs.filter(fecha_creacion__gte=fecha_inicio)
    if fecha_fin:
        ventas_qs = ventas_qs.filter(fecha_creacion__lte=fecha_fin)

     # Preparar la consulta inicial para DetalleVenta
    detalles_qs = DetalleVenta.objects.filter(venta__in=ventas_qs)

    # Aplicar filtro de producto en DetalleVenta
    if filtro_producto:
        detalles_qs = detalles_qs.filter(producto__nombre__icontains=filtro_producto)

     # Agregando a nivel de producto
    datos_agrupados = detalles_qs.values(
        'producto_id', 'producto__nombre'
    ).annotate(
        cantidad_total=Sum('cantidad'),
        costo_total=Sum(F('cantidad') * F('precio_compra_en_venta')),
        ventas_total=Sum((F('cantidad') * F('precio')) - F('descuento')),
        renta_bruta=ExpressionWrapper(F('ventas_total') - F('costo_total'), output_field=DecimalField()),
        porcentaje_renta=ExpressionWrapper(F('renta_bruta') / F('ventas_total') * 100, output_field=DecimalField())
    )


    datos_ventas = [
        {
            'producto_id': dato['producto_id'],
            'nombre_producto': dato['producto__nombre'],
            'cantidad': dato['cantidad_total'],
            'costo_total': dato['costo_total'],
            'ventas_total': dato['ventas_total'],
            'renta_bruta': dato['renta_bruta'],
            'porcentaje_renta': dato['porcentaje_renta'],
        }
        for dato in datos_agrupados
    ]

    # Cálculos de totales
    total_cant = sum(item['cantidad'] for item in datos_ventas)
    total_costos = sum(item['costo_total'] for item in datos_ventas)
    total_ventas = sum(item['ventas_total'] for item in datos_ventas)
    total_renta = sum(item['renta_bruta'] for item in datos_ventas)
    porcentaje_total = (total_ventas - total_costos) / total_ventas * 100 if total_ventas else 0

    # Renderizar la plantilla HTML con los datos
    html_string = render_to_string('Ventas/reporte_ventas.html', {
        'ventas': datos_ventas,
        'total_cant': total_cant,
        'total_costos': total_costos,
        'total_ventas': total_ventas,
        'total_renta': total_renta,
        'porcentaje_total': porcentaje_total,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
        'filtro_cliente': filtro_cliente,
         'filtro_producto': filtro_producto,
        'filtro_vendedor': filtro_vendedor,
    })

    # Crear un PDF usando WeasyPrint
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Crear una respuesta HTTP con el PDF
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    return response



@login_required
def buscar_cliente2(request):
    termino_busqueda = request.GET.get('q', '')
    clientes = Cliente.objects.filter(nombre__icontains=termino_busqueda).values('nombre')[:10]  # Limita los resultados a 10
    return JsonResponse(list(clientes), safe=False)

login_required()
def buscar_producto3(request):
    termino_busqueda = request.GET.get('q', '')
    producto = Producto.objects.filter(nombre__icontains=termino_busqueda).values('nombre')[:10]  # Limita los resultados a 10
    return JsonResponse(list(producto), safe=False)

@login_required
def generar_recibo_pdf(request, pk_cobro):
    # Toma los mismos pasos para obtener los datos del recibo como lo harías normalmente
    cobro = get_object_or_404(Cobro, pk=pk_cobro)
    venta = cobro.venta
    detalles_venta = venta.detalles.all()
    otros_cobros = Cobro.objects.filter(venta=venta).exclude(pk=pk_cobro).select_related('vendedor')

    # Calcula la suma de todos los cobros excepto el actual
    total_abonado = otros_cobros.aggregate(Sum('monto'))['monto__sum'] or 0

    # Renderiza el HTML para el recibo
    html_string = render_to_string('Ventas/recibo_pdf.html', {
        'venta': venta,
        'detalles_venta': detalles_venta,
        'cobro_actual': cobro,
        'otros_cobros': otros_cobros,
        'total_abonado': total_abonado,
    })
    
     # Crear un PDF usando WeasyPrint
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Crear una respuesta HTTP con el PDF
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recibo.pdf"'

    return response


@login_required
def buscar_cliente3(request):
    search_term = request.GET.get('search', '')
    if search_term:
        clientes = Cliente.objects.filter(nombre__icontains=search_term)
    else:
        clientes = Cliente.objects.all()

    return render(request, 'Ventas/ventas_credito_cliente.html', {'clientes': clientes})