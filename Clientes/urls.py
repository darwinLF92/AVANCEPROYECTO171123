from django.urls import path
from . import views
from .views import detalle_credito_cliente

app_name = 'Clientes'  # Este es el espacio de nombres de la aplicación

urlpatterns = [
    path('nuevo/', views.cliente_create_view, name='cliente-create'),
    path('editar/<int:pk>/', views.cliente_edit_view, name='cliente-edit'),
    path('eliminar/<int:pk>/', views.cliente_delete_view, name='cliente-delete'),
    path('lista/', views.cliente_list_view, name='cliente-list'),
    path('Clientes/<int:cliente_id>/credito/', detalle_credito_cliente, name='detalle_credito_cliente'),
]
