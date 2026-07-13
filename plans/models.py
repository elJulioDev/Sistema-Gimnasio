from django.db import models

class PlanCategory(models.TextChoices):
    GENERAL = 'general', 'General'
    ESTUDIANTE = 'estudiante', 'Estudiante'
    MUNICIPAL = 'municipal', 'Trabajador Municipal'
    OTRO = 'otro', 'Otro'

class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=PlanCategory.choices, default=PlanCategory.GENERAL)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

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