from django.conf import settings
from django.db import models

class ExerciseLog(models.Model):
    routine_exercise = models.ForeignKey('routines.RoutineExercise', related_name='logs', on_delete=models.CASCADE)
    fecha = models.DateField()
    series_logradas = models.PositiveIntegerField()
    repeticiones_logradas = models.PositiveIntegerField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.routine_exercise} - {self.fecha}"

class CardioLog(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cardio_logs', on_delete=models.CASCADE)
    fecha = models.DateField()
    minutos = models.PositiveIntegerField()
    calorias_estimadas = models.PositiveIntegerField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha} ({self.minutos} min)"