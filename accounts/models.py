from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administración'
        RECEPCION = 'recepcion', 'Recepción'
        CLIENTE = 'cliente', 'Cliente'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENTE)
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True)
    apellido_materno = models.CharField(max_length=50, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    estudios = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20)
    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_base64 = models.TextField(blank=True)