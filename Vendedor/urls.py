from django.urls import path
from .views import ListaVendedoresView, CrearVendedorView, EditarVendedorView, CambiarEstadoVendedorView
app_name = 'Vendedor'

urlpatterns = [

    path('vendedores/', ListaVendedoresView.as_view(), name='lista_vendedores'),
    path('vendedor/crear/', CrearVendedorView.as_view(), name='crear_vendedor'),
    path('vendedor/editar/<int:vendedor_id>/', CrearVendedorView.as_view(), name='editar_vendedor'),
    path('vendedores/cambiar-estado/<int:pk>/', CambiarEstadoVendedorView.as_view(), name='cambiar_estado_vendedor'),

]

