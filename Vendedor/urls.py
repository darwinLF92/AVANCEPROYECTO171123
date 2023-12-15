from django.urls import path
from . import views
from .views import ListaVendedoresView,CambiarEstadoVendedorView, buscar_vendedor
app_name = 'Vendedor'


urlpatterns = [

    path('vendedores/', ListaVendedoresView.as_view(), name='lista_vendedores'),
    path('crear_vendedor/', views.crear_vendedor, name='crear_vendedor'),
    path('vendedores/cambiar-estado/<int:pk>/', CambiarEstadoVendedorView.as_view(), name='cambiar_estado_vendedor'),
     path('buscar-vendedor/', buscar_vendedor, name='buscar_vendedor'),
     path('vendedor/editar/<int:vendedor_id>/', views.editar_vendedores, name='editar_vendedores'),
      path('vendedor/creado-exito/', views.vendedor_creado_exito, name='vendedor_creado_exito'),
     path('vendedor/editado-exito/', views.vendedor_editado_exito, name='vendedor_editado_exito'),

]

