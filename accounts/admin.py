from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    readonly_fields = UserAdmin.readonly_fields + ('qr_preview',)

    def qr_preview(self, obj):
        if obj.qr_base64:
            return format_html('<img src="data:image/png;base64,{}" width="150">', obj.qr_base64)
        return '-'
    qr_preview.short_description = 'QR'

admin.site.register(CustomUser, CustomUserAdmin)