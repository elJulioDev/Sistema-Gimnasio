from datetime import timedelta
from django.utils import timezone

def calcular_racha_actual(usuario):
    fechas = set(
        usuario.checkins.filter(acceso_valido=True)
        .values_list('fecha_hora__date', flat=True)
    )
    cursor = timezone.localdate()
    racha = 0
    hoy_pendiente = True

    while True:
        # domingo no cuenta ni rompe racha
        if cursor.weekday() == 6:
            cursor -= timedelta(days=1)
            continue
        if cursor in fechas:
            racha += 1
            hoy_pendiente = False
        elif hoy_pendiente:
            hoy_pendiente = False
        else:
            break
        cursor -= timedelta(days=1)

    return racha