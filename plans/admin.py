from django.contrib import admin
from .models import Plan, PlanDetail

class PlanDetailInline(admin.TabularInline):
    model = PlanDetail
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_mensual', 'activo')
    list_filter = ('categoria', 'activo')
    inlines = [PlanDetailInline]