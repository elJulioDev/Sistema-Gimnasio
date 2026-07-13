from django.conf import settings
from django.db import models
from plans.models import Subscription

class MetodoPago(models.TextChoices):
    TARJETA_DEBITO = 'tarjeta_debito', 'Tarjeta Débito (presencial)'
    MERCADOPAGO = 'mercadopago', 'MercadoPago'
    CUENTA_RUT = 'cuenta_rut', 'Cuenta RUT'
    PAYPAL = 'paypal', 'PayPal'

class PaymentStatus(models.TextChoices):
    PENDIENTE = 'pendiente', 'Pendiente'
    APROBADO = 'aprobado', 'Aprobado'
    RECHAZADO = 'rechazado', 'Rechazado'

class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, related_name='pagos', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices)
    estado = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDIENTE)
    referencia_externa = models.CharField(max_length=100, blank=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='pagos_registrados',
        null=True, blank=True, on_delete=models.SET_NULL
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription.usuario} - {self.monto} ({self.estado})"