from django.contrib import admin
from .models import Machine, Routine, RoutineDay, RoutineExercise

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'activa')
    list_filter = ('categoria', 'activa')
    search_fields = ('nombre',)

class RoutineExerciseInline(admin.TabularInline):
    model = RoutineExercise
    extra = 1

class RoutineDayInline(admin.TabularInline):
    model = RoutineDay
    extra = 1

@admin.register(RoutineDay)
class RoutineDayAdmin(admin.ModelAdmin):
    list_display = ('routine', 'dia_semana')
    inlines = [RoutineExerciseInline]

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre', 'activa', 'creado')
    list_filter = ('activa',)
    search_fields = ('usuario__username', 'nombre')