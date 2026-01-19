from django.contrib import admin
from .models import Factura, DetalleFactura


class DetalleInline(admin.TabularInline):
    model = DetalleFactura
    extra = 0


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('codigo_factura', 'cliente', 'cajero', 'barbero', 'fecha', 'total')
    inlines = [DetalleInline]
