from django.db import models


class Corte(models.Model):
    nombre_corte = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre_corte} - {self.precio}"
