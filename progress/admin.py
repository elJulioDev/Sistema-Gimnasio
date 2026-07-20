from django.contrib import admin
from .models import ExerciseLog, CardioLog

@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('routine_exercise', 'fecha', 'series_logradas', 'repeticiones_logradas')
    list_filter = ('fecha',)

@admin.register(CardioLog)
class CardioLogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'minutos', 'calorias_estimadas')
    list_filter = ('fecha',)