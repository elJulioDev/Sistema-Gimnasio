from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    readonly_fields = UserAdmin.readonly_fields + ('qr_preview',)
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = UserAdmin.list_filter + ('role',)

    fieldsets = UserAdmin.fieldsets + (
        ('Datos del sistema', {
            'fields': ('role', 'rut', 'apellido_materno', 'fecha_nacimiento', 'edad', 'estudios', 'telefono', 'qr_preview')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos del sistema', {
            'fields': ('role', 'rut', 'telefono', 'email')
        }),
    )

    def qr_preview(self, obj):
        if obj.qr_base64:
            return format_html('<img src="data:image/png;base64,{}" width="150">', obj.qr_base64)
        return '-'
    qr_preview.short_description = 'QR'

admin.site.register(CustomUser, CustomUserAdmin)