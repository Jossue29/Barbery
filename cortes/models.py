from django.db import models


class Corte(models.Model):
    nombre_corte = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre_corte} - {self.precio}"
