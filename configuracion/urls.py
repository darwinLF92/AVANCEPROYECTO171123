from django.urls import path
from .views import ConfiguracionCreateView, ConfiguracionUpdateView, mostrar_configuracion

app_name = 'Configuracion'  # Este es el espacio de nombres de la aplicación

urlpatterns = [
    path('nueva/', ConfiguracionCreateView.as_view(), name='configuracion_nueva'),
    path('configuracion/editar/', ConfiguracionUpdateView.as_view(), name='configuracion_editar'),

    path('configuracion/', mostrar_configuracion, name='mostrar_configuracion'),

]