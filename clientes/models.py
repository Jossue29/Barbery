from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.nombre} - {self.telefono}"
