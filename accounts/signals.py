import qrcode
import base64
from io import BytesIO
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def generar_qr(sender, instance, created, **kwargs):
    if created and not instance.qr_base64:
        qr = qrcode.make(str(instance.qr_token))
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        instance.qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        instance.save(update_fields=['qr_base64'])