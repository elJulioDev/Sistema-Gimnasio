from django.contrib import admin
from .models import Plan, PlanDetail
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'plan', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'plan')
    search_fields = ('usuario__username', 'usuario__email')

class PlanDetailInline(admin.TabularInline):
    model = PlanDetail
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('orden', 'nombre', 'descripcion_breve', 'precio_mensual', 'activo')
    list_display_links = ('nombre',) 
    list_editable = ('orden', 'activo') 
    list_filter = ('tipo', 'activo')
    inlines = [PlanDetailInline]