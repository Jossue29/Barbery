from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROL_CHOICES = [
        ('ADMIN', 'Admin'),
        ('CAJERO', 'Cajero'),
        ('BARBERO', 'Barbero'),
        ('ESTILISTA', 'Estilista'),
    ]

    nombre = models.CharField(max_length=150, blank=True)
    apellido = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    identidad = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='CAJERO')

    def save(self, *args, **kwargs):
        # Si es superuser, forzamos rol ADMIN
        if self.is_superuser:
            self.rol = 'ADMIN'
        super().save(*args, **kwargs)

    def __str__(self):
        # Mostramos username y nombre completo si hay
        full_name = f"{self.nombre} {self.apellido}".strip()
        if full_name:
            return f"{self.username} ({full_name})"
        return self.username
