from django.urls import path
from .views import proveedor_create_view, proveedor_list_view, proveedor_edit_view, proveedor_delete_view

app_name = 'Proveedor'

urlpatterns = [
    path('proveedor/new/', proveedor_create_view, name='proveedor-create'),
    path('proveedores/', proveedor_list_view, name='proveedor-list'),
    path('proveedor/edit/<int:pk>/', proveedor_edit_view, name='proveedor-edit'),
    path('proveedor/delete/<int:pk>/', proveedor_delete_view, name='proveedor-delete'),
]