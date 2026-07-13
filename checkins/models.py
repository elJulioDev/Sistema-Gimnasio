from django.conf import settings
from django.db import models

class GymCheckIn(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='checkins', on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='checkins_registrados',
        null=True, blank=True, on_delete=models.SET_NULL
    )
    acceso_valido = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha_hora}"