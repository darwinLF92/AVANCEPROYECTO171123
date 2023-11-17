from django.urls import path
from . import views
from .views import VentasView, AutocompleteView


app_name = 'Ventas'

urlpatterns = [
    path('create_venta/', views.create_venta, name='create_venta'),
    path('lista-ventas/', views.lista_ventas, name='lista_ventas'),
    # Asumiendo que tienes una vista para ver los detalles de una venta específica
    path('detalle-venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('add_sale/', views.AddVentaView.as_view(), name='AddSale'),
    path('ventas/crear/', VentasView.as_view(), name='crearventa'),
    path('autocomplete/', AutocompleteView.as_view(), name='autocomplete'),
    path('venta/', views.create_ventas, name='crear'),
    #path('buscar-producto/', views.buscar_producto, name='buscar_producto'),
    path('ruta/busqueda/productos/', views.buscar_productos, name='buscar_productos'),
    path('ruta/busqueda/clientes/', views.buscar_clientes, name='buscar_clientes'),


]
