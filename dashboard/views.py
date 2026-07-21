from django.shortcuts import render
from accounts.decorators import role_required
from accounts.models import CustomUser
from plans.models import Subscription, SubscriptionStatus
from progress.services import (
    calcular_racha_actual, checkins_del_mes, checkins_recientes,
    formatear_checkins, semana_actual_asistencia, calorias_semana,
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
    return render(request, 'dashboard/cliente_plan.html')

@role_required(CustomUser.Role.CLIENTE)
def cliente_progreso(request):
    return render(request, 'dashboard/cliente_progreso.html')

@role_required(CustomUser.Role.CLIENTE)
def cliente_perfil(request):
    return render(request, 'dashboard/cliente_perfil.html')