from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_clientes, name='clientes_list'),
    path('api/search/', views.api_search_cliente, name='api_search_cliente'),
    path('ajax/buscar/', views.buscar_cliente_ajax, name='buscar_cliente_ajax'),
    # path('api/create/', views.api_create_cliente, name='api_create_cliente'),
    path('ajax/crear/', views.crear_cliente_ajax, name='crear_cliente_ajax'),
]
