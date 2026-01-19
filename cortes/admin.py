from django.contrib import admin
from .models import Corte


@admin.register(Corte)
class CorteAdmin(admin.ModelAdmin):
    list_display = ('nombre_corte', 'precio')
    search_fields = ('nombre_corte',)
