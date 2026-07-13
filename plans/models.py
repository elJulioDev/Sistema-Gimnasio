from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class PlanCategory(models.TextChoices):
    GENERAL = 'general', 'General'
    ESTUDIANTE = 'estudiante', 'Estudiante'
    MUNICIPAL = 'municipal', 'Trabajador Municipal'
    OTRO = 'otro', 'Otro'

class PlanType(models.TextChoices):
    MENSUAL = 'mensual', 'Mensual'
    DIA = 'dia', 'Pase Diario'

class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=PlanCategory.choices, default=PlanCategory.GENERAL)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=PlanType.choices, default=PlanType.MENSUAL)

    def __str__(self):
        return self.nombre

class PlanDetail(models.Model):
    plan = models.ForeignKey(Plan, related_name='detalles', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.plan.nombre} - {self.descripcion}"

class SubscriptionStatus(models.TextChoices):
    ACTIVA = 'activa', 'Activa'
    VENCIDA = 'vencida', 'Vencida'
    CANCELADA = 'cancelada', 'Cancelada'

class Subscription(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='suscripciones', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, related_name='suscripciones', on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.ACTIVA)
    auto_renovacion = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    @property
    def esta_vigente(self):
        return self.estado == SubscriptionStatus.ACTIVA and self.fecha_fin >= timezone.now().date()

    def renovar(self):
        self.fecha_inicio = timezone.now().date()
        self.fecha_fin = self.fecha_inicio + timedelta(days=30)
        self.estado = SubscriptionStatus.ACTIVA
        self.save()

    def __str__(self):
        return f"{self.usuario} - {self.plan.nombre} ({self.estado})"