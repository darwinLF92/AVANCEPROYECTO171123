from decimal import Decimal, InvalidOperation
from pyexpat.errors import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.db import transaction
from .models import Producto, ComponenteProducto, Transaccion
from .forms import ProductoForm, ComponenteProductoForm, ProductoPrincipalForm
from django.http import JsonResponse
from django.forms import DecimalField, model_to_dict, modelformset_factory, inlineformset_factory
from django.db.models import ExpressionWrapper
from datetime import datetime
from .models import Proveedor
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import FileResponse, JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def listar_productos(request):
    nombre = request.GET.get('nombre', '')

    # Filtrar los productos por nombre si se proporciona un valor de búsqueda
    if nombre:
        productos = Producto.objects.filter(activo=True, nombre__icontains=nombre)
    else:
        # Si no se proporciona un valor de búsqueda, mostrar todos los productos activos
        productos = Producto.objects.filter(activo=True)

        # Número de elementos por página
    elementos_por_pagina = 10
    # Paginación
    paginator = Paginator(productos, elementos_por_pagina)  # Muestra 10 productos por página

    page = request.GET.get('page')
    try:
        productos_paginados = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        productos_paginados = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por ejemplo, 9999), muestra la última página
        productos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'Producto/listar_productos.html', {'productos': productos_paginados, 'nombre': nombre})



def get_productos(request):
    producto = Producto.objects.filter(activo=True).values('nombre', 'precio_compra')
    return JsonResponse(list(producto), safe=False)
 


#para ver la lista de productos marcados como fabricacion
def listar_productos_fabricacion(request):
    # Obtén todos los productos para fabricación activos
    productos_para_fabricacion = Producto.objects.filter(activo=True, para_fabricacion=True)

    # Número de productos por página
    productos_por_pagina = 10  # Puedes ajustar esto según tus necesidades

    # Configura el paginador
    paginator = Paginator(productos_para_fabricacion, productos_por_pagina)

    # Obtiene el número de página actual desde la solicitud GET
    page = request.GET.get('page')

    try:
        # Obtiene los productos para la página actual
        productos = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        productos = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (por ejemplo, 9999), muestra la última página
        productos = paginator.page(paginator.num_pages)

    return render(request, 'Producto/lista_productos_prod.html', {'productos': productos})


def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            
            return render(request, 'Producto/agregar_producto.html', {'success': True, 'message': f'Producto creado satisfactoriamente'})
        else:
            # Si el formulario de producto no es válido, muestra los errores en la misma página.
            return render(request, 'Producto/agregar_producto.html', {'form': form})
    else:
        form = ProductoForm()
        return render(request, 'Producto/agregar_producto.html', {'form': form})


def editar_producto(request, producto_id):
    # Obtén el producto que quieres editar o manda un error 404 si no existe
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        # Crea una instancia del formulario y rellénalo con los datos de la petición (binding):
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            # Guarda el producto editado en la base de datos
            form.save()
            # Redirige a la lista de productos o a la vista de detalles del producto
            return render(request, 'Producto/agregar_producto.html', {'success': True, 'message': f'Producto editado satisfactoriamente'})
    else:
        # Crea el formulario con los datos del producto que se va a editar
        form = ProductoForm(instance=producto)

    # Renderiza la plantilla con el formulario
    return render(request, 'Producto/editar_producto.html', {'form': form, 'producto': producto})


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = False  # Suponiendo que tienes un campo "activo" en el modelo Producto
    producto.save()
    return redirect('Producto:listar_productos')


@transaction.atomic  # Asegura que las operaciones sean atómicas
def aumentar_stock(request, producto_id):
    producto_principal = get_object_or_404(Producto, id=producto_id)
    if producto_principal.para_fabricacion:  # Asegúrate de que este campo exista en tu modelo Producto
        if request.method == 'POST':
            cantidad_a_fabricar = int(request.POST.get('cantidad', 0))  # Asegúrate de validar este valor correctamente.
            
            # Inicia una lista para controlar si todos los componentes tienen stock suficiente
            componentes_insuficientes = []

            # Verifica si hay suficientes componentes para la cantidad a fabricar
            for componente in ComponenteProducto.objects.filter(producto_principal=producto_principal):
                if componente.cantidad * cantidad_a_fabricar > componente.producto_componente.stock:
                    componentes_insuficientes.append(componente.producto_componente.nombre)
            
            if not componentes_insuficientes:
                # Actualiza el stock del producto principal
                producto_principal.stock += cantidad_a_fabricar
                producto_principal.save()

                # Disminuir la cantidad de materia prima
                for componente in ComponenteProducto.objects.filter(producto_principal=producto_principal):
                    producto_componente = componente.producto_componente
                    producto_componente.stock -= componente.cantidad * cantidad_a_fabricar
                    producto_componente.save()

                # Registra la transacción
                Transaccion.objects.create(
                    producto=producto_principal,
                    cantidad=cantidad_a_fabricar,
                    # La fecha de registro se añade automáticamente con auto_now_add=True en el modelo
                )
                
                return render(request, 'Producto/aumentar_stock.html', {'success': True, 'message': f'Producto aumentado satisfactoriamente'})
            else:
                # Manejar la falta de componentes mostrando un mensaje al usuario
                # Podrías añadir un mensaje al contexto para informar qué componentes no tienen stock suficiente
                return render(request, 'Producto/aumentar_stock.html', {
                    'producto': producto_principal,
                    'error': f"No hay suficiente stock para los componentes: {', '.join(componentes_insuficientes)}."
                })

        return render(request, 'Producto/aumentar_stock.html', {'producto': producto_principal})
    else:
        # Si el producto no es fabricable, redireccionar o mostrar un mensaje de error
        return redirect('Producto:listar_productos')
    
    
def ver_detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    componentes = ComponenteProducto.objects.filter(producto_principal=producto).select_related('producto_componente')
    
    # Crear una lista de componentes con su nombre y la cantidad necesaria para la fabricación del producto
    lista_componentes = [
        {
            'nombre': componente.producto_componente.nombre,
            'cantidad_necesaria': componente.cantidad,
            'stock_actual': componente.producto_componente.stock
        }
        for componente in componentes
    ]

    context = {
        'producto': producto,
        'componentes': lista_componentes
    }

    return render(request, 'Producto/ver_detalle_producto.html', context)



from django.db.models import F, Sum

def editar_componentes_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
   
    ComponenteProductoFormSet = inlineformset_factory(
        Producto, 
        ComponenteProducto, 
        form=ComponenteProductoForm, 
        fields=('producto_componente', 'cantidad'), 
        extra=1,
        can_delete=True,
        fk_name='producto_principal'
    )
    
    if request.method == 'POST':
        formset = ComponenteProductoFormSet(request.POST, instance=producto, prefix='componentes')
        if formset.is_valid():
            formset.save()

            # Calcular el costo total de producción después de guardar el formset
            costo_total_produccion = producto.componentes_principal.annotate(
                total_cost=F('cantidad') * F('producto_componente__precio_compra')
            ).aggregate(Sum('total_cost'))['total_cost__sum'] or 0

            # Establecer el costo total de producción como el nuevo precio de compra
            producto.precio_compra = costo_total_produccion
            producto.save()

            
            return render(request, 'Producto/editar_componentes_producto.html', {'success': True, 'message': f'Componente editado satisfactoriamente'})
            
    else:
        formset = ComponenteProductoFormSet(instance=producto, prefix='componentes')

        # Calcular el costo total de producción para mostrarlo en el formulario, pero no guardarlo aún
        costo_total_produccion = producto.componentes_principal.annotate(
            total_cost=F('cantidad') * F('producto_componente__precio_compra')
        ).aggregate(Sum('total_cost'))['total_cost__sum'] or 0

    return render(request, 'Producto/editar_componentes_producto.html', {
        'formset': formset,
        'producto': producto,
        'costo_total_produccion': costo_total_produccion,
        
    })

def producto_search_view(request):
    nombre = request.GET.get('nombre', '')

    if nombre:
        productos = Producto.objects.filter(activo=True, nombre__icontains=nombre)
    else:
        productos = Producto.objects.filter(activo=True)

    return render(request, 'Producto/listar_productos.html', {'productos': productos, 'nombre': nombre})

def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query)[:10]  # limitamos a 10 resultados
    productos_json = [
        {'id': prod.id, 'nombre': prod.nombre, 'precio': prod.precio_venta, 'stock': prod.stock}
        for prod in productos
    ]
    return JsonResponse(productos_json, safe=False)


def reporte_inventario(request):
    proveedores = list(Proveedor.objects.filter(activo=True).values_list('nombre', flat=True))
    filtro_producto = request.GET.get('producto', '')
    filtro_tipo_producto = request.GET.get('tipoproducto', '')
    filtro_proveedor = request.GET.get('proveedor', '')
    filtro_stock = request.GET.get('stock', '')
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')

    productos_qs = Producto.objects.filter(activo=True)

    estados_stock = [
        {'nombre': 'Con Existencia', 'valor': 'con_existencia'},
        {'nombre': 'Sin Existencia', 'valor': 'sin_existencia'}
    ]

    tipos_producto = [
        {'nombre': 'Materia Prima', 'valor': 'materia_prima'},
        {'nombre': 'Para Fabricación', 'valor': 'para_fabricacion'},
        {'nombre': 'Producto Terminado', 'valor': 'producto_terminado'}
    ]

    # Filtrar por nombre de producto
    if filtro_producto:
        productos_qs = productos_qs.filter(nombre__icontains=filtro_producto)

    # Filtrar por tipo de producto
    if filtro_tipo_producto:
        if filtro_tipo_producto == 'materia_prima':
            productos_qs = productos_qs.filter(es_materia_prima=True)
        elif filtro_tipo_producto == 'para_fabricacion':
            productos_qs = productos_qs.filter(para_fabricacion=True)
        elif filtro_tipo_producto == 'producto_terminado':
            productos_qs = productos_qs.filter(es_materia_prima=False, para_fabricacion=False)

    # Filtrar por proveedor
    if filtro_proveedor:
        productos_qs = productos_qs.filter(proveedor__nombre__icontains=filtro_proveedor)

    # Filtrar por stock
    if filtro_stock:
        if filtro_stock == 'con_existencia':
            productos_qs = productos_qs.filter(stock__gt=0)
        elif filtro_stock == 'sin_existencia':
            productos_qs = productos_qs.filter(stock__lte=0)

    # Agregando datos de inventario
    datos_inventario = productos_qs.values(
        'id', 'codigo', 'nombre', 'stock', 'precio_compra', 'precio_venta'
    ).annotate(
        total_costo=Sum(F('stock') * F('precio_compra')),
        total_venta=Sum(F('stock') * F('precio_venta')),
    )

    datos_productos = [
        {
            'producto_id': dato['id'],
            'codigo': dato['codigo'],
            'nombre': dato['nombre'],
            'stock': dato['stock'],
            'precio_compra': dato['precio_compra'],
            'precio_venta': dato['precio_venta'],
            'total_costo': dato['total_costo'],
            'total_venta': dato['total_venta'],
        }
        for dato in datos_inventario
    ]

    # Cálculos de totales
    # Cálculos de totales
    total_stock = sum(item['stock'] for item in datos_productos)
    total_costos = sum(item['total_costo'] for item in datos_productos)
    total_ventas = sum(item['total_venta'] for item in datos_productos)

    return JsonResponse({
        'productos': datos_productos,
        'total_stock': total_stock,
        'total_costos': total_costos,
        'total_ventas': total_ventas,
        'fecha_hoy': fecha_hoy,
        'proveedores': proveedores,
        'estadosStock': estados_stock, 
        'tiposProducto': tipos_producto
    })


def buscar_producto2(request):
    termino_busqueda = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=termino_busqueda).values('nombre')[:10]  # Limita los resultados a 10
    return JsonResponse(list(productos), safe=False)



def reporte_inventariofinanciero_pdf(request):
    # Obtener lista de vendedores activos
    proveedores = list(Proveedor.objects.filter(activo=True).values_list('nombre', flat=True))
    filtro_producto = request.GET.get('producto', '')
    filtro_tipo_producto = request.GET.get('tipoproducto', '')
    filtro_proveedor = request.GET.get('proveedor', '')
    filtro_stock = request.GET.get('stock', '')
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')

    productos_qs = Producto.objects.filter(activo=True)

    estados_stock = [
        {'nombre': 'Con Existencia', 'valor': 'con_existencia'},
        {'nombre': 'Sin Existencia', 'valor': 'sin_existencia'}
    ]

    tipos_producto = [
        {'nombre': 'Materia Prima', 'valor': 'materia_prima'},
        {'nombre': 'Para Fabricación', 'valor': 'para_fabricacion'},
        {'nombre': 'Producto Terminado', 'valor': 'producto_terminado'}
    ]

    # Filtrar por nombre de producto
    if filtro_producto:
        productos_qs = productos_qs.filter(nombre__icontains=filtro_producto)

    # Filtrar por tipo de producto
    if filtro_tipo_producto:
        if filtro_tipo_producto == 'materia_prima':
            productos_qs = productos_qs.filter(es_materia_prima=True)
        elif filtro_tipo_producto == 'para_fabricacion':
            productos_qs = productos_qs.filter(para_fabricacion=True)
        elif filtro_tipo_producto == 'producto_terminado':
            productos_qs = productos_qs.filter(es_materia_prima=False, para_fabricacion=False)

    # Filtrar por proveedor
    if filtro_proveedor:
        productos_qs = productos_qs.filter(proveedor__nombre__icontains=filtro_proveedor)

    # Filtrar por stock
    if filtro_stock:
        if filtro_stock == 'con_existencia':
            productos_qs = productos_qs.filter(stock__gt=0)
        elif filtro_stock == 'sin_existencia':
            productos_qs = productos_qs.filter(stock__lte=0)

    # Agregando datos de inventario
    datos_inventario = productos_qs.values(
        'id', 'codigo', 'nombre', 'stock', 'precio_compra', 'precio_venta'
    ).annotate(
        total_costo=Sum(F('stock') * F('precio_compra')),
        total_venta=Sum(F('stock') * F('precio_venta')),
    )

    datos_productos = [
        {
            'producto_id': dato['id'],
            'codigo': dato['codigo'],
            'nombre': dato['nombre'],
            'stock': dato['stock'],
            'precio_compra': dato['precio_compra'],
            'precio_venta': dato['precio_venta'],
            'total_costo': dato['total_costo'],
            'total_venta': dato['total_venta'],
        }
        for dato in datos_inventario
    ]

    # Cálculos de totales
    # Cálculos de totales
    total_stock = sum(item['stock'] for item in datos_productos)
    total_costos = sum(item['total_costo'] for item in datos_productos)
    total_ventas = sum(item['total_venta'] for item in datos_productos)

    # Renderizar la plantilla HTML con los datos
    html_string = render_to_string('Producto/reporte_inventario_financiero.html', {
        'productos': datos_productos,
        'total_stock': total_stock,
        'total_costos': total_costos,
        'total_ventas': total_ventas,
        'fecha_hoy': fecha_hoy,
        'filtro_producto': filtro_producto,
        'filtro_proveedor': filtro_proveedor,
        'filtro_stock': filtro_stock,
        'filtro_tipoproducto': filtro_tipo_producto
    })

    # Crear un PDF usando WeasyPrint
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Crear una respuesta HTTP con el PDF
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario_financiero.pdf"'

    return response


def reporte_inventario_pdf(request):
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')

    # Filtrar productos activos con stock mayor a cero
    productos_qs = Producto.objects.filter(activo=True, stock__gt=0).order_by('nombre')

    # Obtener datos necesarios de inventario
    datos_inventario = productos_qs.values('id', 'codigo', 'nombre', 'stock')

    datos_productos = [
        {
            'producto_id': dato['id'],
            'codigo': dato['codigo'],
            'nombre': dato['nombre'],
            'stock': dato['stock'],
        }
        for dato in datos_inventario
    ]

    # Cálculo del total de stock
    total_stock = sum(item['stock'] for item in datos_productos)

    # Renderizar la plantilla HTML con los datos
    html_string = render_to_string('Producto/reporte_inventario.html', {
        'productos': datos_productos,
        'total_stock': total_stock,
        'fecha_hoy': fecha_hoy,
    })

    # Crear un PDF usando WeasyPrint
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Crear una respuesta HTTP con el PDF
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'

    return response


