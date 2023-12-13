from django.urls import path
from . import views
from .views import VentasCreditoPorClienteView, DetalleVentasCreditoClienteView, generar_recibo, CobrosListView, procesar_cobro, ListaVentasView
from .views import imprimir_venta, reporte_cuentasxcobrar_pdf, reporte_cuentasxcobrar, reporte_cobros_pdf, reporte_ventas_pdf



app_name = 'Ventas'

urlpatterns = [

    path('lista-ventas/', views.ListaVentasView.as_view(), name='lista_ventas'),
    # Asumiendo que tienes una vista para ver los detalles de una venta específica
    path('detalle-venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('add_sale/', views.AddVentaView.as_view(), name='AddSale'),
    path('venta/eliminar/<int:id>/', views.eliminar_venta, name='confirmar_eliminar_venta'),
    path('ruta/busqueda/productos/', views.buscar_productos, name='buscar_productos'),
    path('ruta/busqueda/clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('ventas-credito-cliente/', VentasCreditoPorClienteView.as_view(), name='ventas_credito_cliente'),
    path('lista_creditos/<int:pk>/', DetalleVentasCreditoClienteView.as_view(), name='lista_creditos'),
    path('Ventas/ruta-para-procesar-cobro', procesar_cobro, name='procesar-cobro'),
    path('recibo/<int:pk_cobro>/', generar_recibo, name='generar_recibo'),
    path('cobros/list', CobrosListView.as_view(), name='cobros-list'),
    path('imprimir-venta/<int:venta_id>/', imprimir_venta, name='imprimir_venta'),
    path('anular-venta/<int:venta_id>/', views.anular_venta, name='anular_venta'),
    path('reporte-cuentasxcobrar/', reporte_cuentasxcobrar, name='reporte_cuentasxcobrar'),
    path('reporte-cuentasxcobrar-pdf/', reporte_cuentasxcobrar_pdf, name='reporte_cuentasxcobrar_pdf'),
    path('reporte-cobros', views.reporte_cobros, name='reporte_cobros'),
    path('anular-cobro/<int:cobro_id>/', views.anular_cobro, name='anular_cobro'),
    path('reporte-cobros-pdf/', reporte_cobros_pdf, name='reporte_cobros_pdf'),
    path('reporte-ventas', views.reporte_ventas, name='reporte_ventas'),
    path('reporte-ventas-pdf/', reporte_ventas_pdf, name='reporte_ventas_pdf'),
    path('buscar-cliente2/', views.buscar_cliente2, name='buscar_cliente2'),
    path('generar-recibo-pdf/<int:pk_cobro>/', views.generar_recibo_pdf, name='generar_recibo_pdf'),
    path('buscar-producto3/', views.buscar_producto3, name='buscar_producto3'),

]
