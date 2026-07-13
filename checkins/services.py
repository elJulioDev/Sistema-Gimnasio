from accounts.models import CustomUser
from plans.models import Subscription, SubscriptionStatus
from .models import GymCheckIn

def procesar_escaneo(qr_token, recepcionista=None):
    try:
        usuario = CustomUser.objects.get(qr_token=qr_token)
    except CustomUser.DoesNotExist:
        return None, "QR inválido"

    suscripcion = Subscription.objects.filter(
        usuario=usuario, estado=SubscriptionStatus.ACTIVA
    ).order_by('-fecha_fin').first()

    valido = bool(suscripcion and suscripcion.esta_vigente)

    GymCheckIn.objects.create(usuario=usuario, registrado_por=recepcionista, acceso_valido=valido)

    mensaje = "Acceso permitido" if valido else "Plan vencido o inexistente"
    return usuario, mensaje