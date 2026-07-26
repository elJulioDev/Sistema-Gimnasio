from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import role_required
from accounts.models import CustomUser
from plans.models import Subscription, SubscriptionStatus
from progress.services import (
    calcular_racha_actual, checkins_del_mes, checkins_recientes,
    formatear_checkins, semana_actual_asistencia, calorias_semana,
    progreso_rutina_activa, historial_cardio,
)

@role_required(CustomUser.Role.ADMIN)
def admin_dashboard(request):
    return render(request, 'dashboard/admin_home.html')

@role_required(CustomUser.Role.CLIENTE)
def cliente_dashboard(request):
    usuario = request.user
    suscripcion = Subscription.objects.filter(
        usuario=usuario, estado=SubscriptionStatus.ACTIVA
    ).select_related('plan').order_by('-fecha_fin').first()

    semana = semana_actual_asistencia(usuario)

    context = {
        'suscripcion': suscripcion,
        'racha_actual': calcular_racha_actual(usuario),
        'checkins_mes': checkins_del_mes(usuario),
        'checkins_recientes': formatear_checkins(checkins_recientes(usuario)),
        'semana': semana,
        'dias_semana_count': sum(1 for d in semana if d['asistio']),
        'calorias_semana': calorias_semana(usuario),
    }
    return render(request, 'dashboard/cliente_home.html', context)

@role_required(CustomUser.Role.CLIENTE)
def cliente_plan(request):
    usuario = request.user
    suscripcion = Subscription.objects.filter(
        usuario=usuario
    ).select_related('plan').order_by('-fecha_fin').first()

    dias_restantes = porcentaje = None
    if suscripcion:
        hoy = timezone.localdate()
        dias_restantes = (suscripcion.fecha_fin - hoy).days
        total_dias = (suscripcion.fecha_fin - suscripcion.fecha_inicio).days or 1
        transcurridos = (hoy - suscripcion.fecha_inicio).days
        porcentaje = max(0, min(100, int(transcurridos / total_dias * 100)))

    return render(request, 'dashboard/cliente_plan.html', {
        'suscripcion': suscripcion,
        'dias_restantes': dias_restantes,
        'porcentaje': porcentaje,
        'pagos': suscripcion.pagos.order_by('-fecha_creacion') if suscripcion else [],
    })

@role_required(CustomUser.Role.CLIENTE)
def cliente_progreso(request):
    usuario = request.user
    return render(request, 'dashboard/cliente_progreso.html', {
        'progreso': progreso_rutina_activa(usuario),
        'cardio_logs': historial_cardio(usuario),
        'calorias_semana': calorias_semana(usuario),
        'racha_actual': calcular_racha_actual(usuario),
    })

@role_required(CustomUser.Role.CLIENTE)
def cliente_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        telefono = request.POST.get('telefono', '').strip()
        if CustomUser.objects.filter(email=email).exclude(pk=usuario.pk).exists():
            messages.error(request, 'Ese correo ya está en uso por otra cuenta.')
        else:
            usuario.email = email
            usuario.telefono = telefono
            usuario.save(update_fields=['email', 'telefono'])
            messages.success(request, 'Datos actualizados correctamente.')
        return redirect('cliente_perfil')
    return render(request, 'dashboard/cliente_perfil.html')