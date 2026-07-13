from django.contrib import admin
from .models import GymCheckIn

@admin.register(GymCheckIn)
class GymCheckInAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_hora', 'registrado_por', 'acceso_valido')
    list_filter = ('acceso_valido',)