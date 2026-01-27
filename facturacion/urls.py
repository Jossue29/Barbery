from django.urls import path
from . import views

urlpatterns = [
    path('', views.historial, name='facturas_historial'),
    path('crear/', views.crear_factura, name='factura_crear'),
    path('api/create/', views.api_create_factura, name='api_create_factura'),
    path('ticket/<int:factura_id>/', views.preview_ticket, name='preview_ticket'),

    #----- cobro ------

    path('cobro/', views.cobro, name='cobro'),
    path('ajax/factura/', views.ajax_cargar_factura, name='ajax_cargar_factura'),
    path('ajax/cobrar/', views.ajax_cobrar_factura, name='ajax_cobrar_factura'),
    path('ajax/mis-cobros/', views.ajax_mis_cobros, name='ajax_mis_cobros'),
    path('historial/', views.historial_facturas, name='historial_facturas'),
    path('ajax/pagar-barbero/', views.pagar_cobros_barbero, name='pagar_cobros_barbero'),

]
