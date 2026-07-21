from datetime import timedelta
from django.db.models import Sum
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

def checkins_del_mes(usuario):
    hoy = timezone.localdate()
    return usuario.checkins.filter(
        acceso_valido=True, fecha_hora__year=hoy.year, fecha_hora__month=hoy.month
    ).count()

def checkins_recientes(usuario, limite=5):
    return usuario.checkins.filter(acceso_valido=True).order_by('-fecha_hora')[:limite]

DIAS_ABREV = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
MESES_ABREV = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

def formatear_checkins(checkins):
    resultado = []
    for c in checkins:
        fecha = timezone.localtime(c.fecha_hora)
        resultado.append({
            'fecha_label': f"{DIAS_ABREV[fecha.weekday()]} {fecha.day} {MESES_ABREV[fecha.month - 1]}",
            'hora_label': fecha.strftime('%H:%M'),
        })
    return resultado

def semana_actual_asistencia(usuario):
    hoy = timezone.localdate()
    lunes = hoy - timedelta(days=hoy.weekday())
    asistidos = set(
        usuario.checkins.filter(
            acceso_valido=True, fecha_hora__date__gte=lunes, fecha_hora__date__lte=hoy
        ).values_list('fecha_hora__date', flat=True)
    )
    letras = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
    dias = []
    for i in range(7):
        fecha = lunes + timedelta(days=i)
        dias.append({
            'letra': letras[i],
            'asistio': fecha in asistidos,
            'es_hoy': fecha == hoy,
            'es_descanso': i == 6,
        })
    return dias

def calorias_semana(usuario):
    hoy = timezone.localdate()
    lunes = hoy - timedelta(days=hoy.weekday())
    total = usuario.cardio_logs.filter(fecha__gte=lunes, fecha__lte=hoy).aggregate(
        total=Sum('calorias_estimadas')
    )['total']
    return total or 0