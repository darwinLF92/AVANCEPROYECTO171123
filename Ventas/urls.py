from django.urls import path
from . import views
from .views import VentasCreditoPorClienteView, DetalleVentasCreditoClienteView, generar_recibo, CobrosListView, procesar_cobro



app_name = 'Ventas'

urlpatterns = [

    path('lista-ventas/', views.lista_ventas, name='lista_ventas'),
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
]
