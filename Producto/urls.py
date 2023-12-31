from django.urls import path
from . import views
from .views import reporte_inventariofinanciero_pdf, reporte_inventario_pdf

app_name = 'Producto'

urlpatterns = [
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('producto/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    #path('agregar_componentes/<int:producto_id>/', views.agregar_componentes, name='agregar_componentes'),
    path('get_productos/', views.get_productos, name='get_productos'),
    path('productos_fabricacion/', views.listar_productos_fabricacion, name='listar_productos_fabricacion'),
    path('producto/<int:producto_id>/aumentar/', views.aumentar_stock, name='aumentar_stock'),
    path('producto/<int:producto_id>/detalle/', views.ver_detalle_producto, name='ver_detalle_producto'),
    #path('productos/seleccionar_principal/', views.seleccionar_producto_principal, name='seleccionar_producto_principal'),
    #path('producto/<int:producto_id>/agregar_componentes/', views.agregar_componentes, name='agregar_componentes'),
    path('producto/<int:producto_id>/editar-componentes/', views.editar_componentes_producto, name='editar_componentes'),
    # Añadir más URLs aquí
    path('producto-search/', views.producto_search_view, name='producto-search'),
    path('ruta/busqueda/productos/', views.buscar_productos, name='buscar_productos'),
    path('reporte-inventario', views.reporte_inventario, name='reporte_inventario'),
    path('buscar-producto2/', views.buscar_producto2, name='buscar_producto2'),
    path('reporte-inventario-financiero-pdf/', reporte_inventariofinanciero_pdf, name='reporte_inventraio_financiero_pdf'),
    path('reporte-inventario-pdf/', reporte_inventario_pdf, name='reporte_inventraio_pdf'),
    path('actualizar-stock/', views.actualizar_stock, name='actualizar_stock'),

]
