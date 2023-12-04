from django.urls import path
from . import views
from .views import historial_ventas


app_name = 'Clientes'  # Este es el espacio de nombres de la aplicación

urlpatterns = [
    path('nuevo/', views.cliente_create_view, name='cliente-create'),
    path('editar/<int:pk>/', views.cliente_edit_view, name='cliente-edit'),
    path('eliminar/<int:pk>/', views.cliente_delete_view, name='cliente-delete'),
    path('lista/', views.cliente_list_view, name='cliente-list'),
    path('cliente-search/', views.cliente_search_view, name='cliente-search'),
    path('clientes/historial_ventas/', views.historial_ventas, name='historial_ventas'),
]
