from django.urls import path
from . import views

urlpatterns = [
    path('', views.historial, name='facturas_historial'),
    path('crear/', views.crear_factura, name='factura_crear'),
    path('api/create/', views.api_create_factura, name='api_create_factura'),
    path('ticket/<int:factura_id>/', views.preview_ticket, name='factura_ticket'),
]
