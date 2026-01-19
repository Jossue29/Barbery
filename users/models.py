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

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
