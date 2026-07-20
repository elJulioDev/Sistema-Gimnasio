from django.conf import settings
from django.db import models

class MachineCategory(models.TextChoices):
    FUERZA = 'fuerza', 'Fuerza'
    CARDIO = 'cardio', 'Cardio'

class Machine(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=10, choices=MachineCategory.choices)
    descripcion = models.CharField(max_length=200, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Routine(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rutinas', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.nombre}"

class DiaSemana(models.IntegerChoices):
    LUNES = 0, 'Lunes'
    MARTES = 1, 'Martes'
    MIERCOLES = 2, 'Miércoles'
    JUEVES = 3, 'Jueves'
    VIERNES = 4, 'Viernes'
    SABADO = 5, 'Sábado'
    DOMINGO = 6, 'Domingo'

class RoutineDay(models.Model):
    routine = models.ForeignKey(Routine, related_name='dias', on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=DiaSemana.choices)

    class Meta:
        unique_together = ('routine', 'dia_semana')

    def __str__(self):
        return f"{self.routine} - {self.get_dia_semana_display()}"

class RoutineExercise(models.Model):
    routine_day = models.ForeignKey(RoutineDay, related_name='ejercicios', on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, related_name='rutina_ejercicios', on_delete=models.PROTECT)
    series_objetivo = models.PositiveIntegerField()
    repeticiones_objetivo = models.PositiveIntegerField()
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.routine_day} - {self.machine}"