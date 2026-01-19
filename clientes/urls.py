from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_clientes, name='clientes_list'),
    path('api/search/', views.api_search_cliente, name='api_search_cliente'),
    path('api/create/', views.api_create_cliente, name='api_create_cliente'),
]
