import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def generar_qr(sender, instance, created, **kwargs):
    if created and not instance.qr_image:
        qr = qrcode.make(str(instance.qr_token))
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        instance.qr_image.save(f'{instance.qr_token}.png', ContentFile(buffer.getvalue()), save=True)