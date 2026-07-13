from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administración'
        RECEPCION = 'recepcion', 'Recepción'
        CLIENTE = 'cliente', 'Cliente'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENTE)