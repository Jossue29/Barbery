from django.db import models
from django.conf import settings
from clientes.models import Cliente
from cortes.models import Corte
import uuid


class Factura(models.Model):
    codigo_factura = models.CharField(max_length=50, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    cajero = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='facturas_cajero')
    barbero = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='facturas_barbero')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.codigo_factura:
            self.codigo_factura = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.codigo_factura} - {self.total}"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    corte = models.ForeignKey(Corte, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.corte} x{self.cantidad} -> {self.subtotal}"
