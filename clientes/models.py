from django.db import models
import re

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(
        max_length=20,
        unique=True
    )

    def save(self, *args, **kwargs):
        if self.telefono:
            self.telefono = re.sub(r'\D+', '', self.telefono)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.telefono}"
