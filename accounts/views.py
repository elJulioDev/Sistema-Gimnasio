from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import IntegrityError, transaction
from datetime import date
from .models import CustomUser
from plans.models import Plan
from django.contrib.auth import login, authenticate
from datetime import date, timedelta
from plans.models import Plan, Subscription, SubscriptionStatus
from payments.models import Payment
from payments.gateways import get_gateway, GatewayNotImplemented
from django.http import JsonResponse
from accounts.models import CustomUser

MIN_AGE = 15

def register(request):
    planes = Plan.objects.filter(activo=True, tipo='mensual').prefetch_related('detalles')

    if request.method == 'POST':
        rut = request.POST.get('rut', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        apellido_materno = request.POST.get('apellido_materno', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        edad = request.POST.get('edad') or None
        estudios = request.POST.get('estudios', '').strip()
        email = request.POST.get('email', '').strip().lower()
        telefono = request.POST.get('telefono', '').strip()
        password = request.POST.get('password')
        confirmar_password = request.POST.get('confirmar_password')
        plan_id = request.POST.get('plan')

        plan = Plan.objects.filter(id=plan_id, activo=True).first()
        if not plan:
            messages.error(request, 'Selecciona un plan válido.')
            return render(request, 'register.html', {'planes': planes})

        if not fecha_nacimiento or not edad or int(edad) < MIN_AGE:
            messages.error(request, f'Debes tener al menos {MIN_AGE} años para registrarte.')
            return render(request, 'register.html', {'planes': planes})

        if password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'register.html', {'planes': planes})

        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'register.html', {'planes': planes})

        if CustomUser.objects.filter(rut=rut).exists():
            messages.error(request, 'Ya existe una cuenta con ese RUT.')
            return render(request, 'register.html', {'planes': planes, 'jump_to_step': 2})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe una cuenta con ese correo.')
            return render(request, 'register.html', {'planes': planes, 'jump_to_step': 2})
        
        metodo_pago = request.POST.get('metodo_pago', 'tarjeta_debito')

        try:
            with transaction.atomic():
                user = CustomUser.objects.create_user(
                    username=rut,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    apellido_materno=apellido_materno,
                    rut=rut,
                    fecha_nacimiento=fecha_nacimiento,
                    edad=edad,
                    estudios=estudios,
                    telefono=telefono,
                    role=CustomUser.Role.CLIENTE,
                )

                fecha_inicio = date.today()
                dias = 1 if plan.tipo == 'dia' else 30
                subscription = Subscription.objects.create(
                    usuario=user,
                    plan=plan,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_inicio + timedelta(days=dias),
                    estado=SubscriptionStatus.ACTIVA,
                )

                payment = Payment.objects.create(
                    subscription=subscription,
                    monto=plan.precio_mensual,
                    metodo_pago=metodo_pago,
                )
                try:
                    get_gateway(metodo_pago).procesar(payment)
                except GatewayNotImplemented:
                    # pasarela placeholder: aprobación automática mientras no exista integración real
                    payment.estado = 'aprobado'
                    payment.save()
        except IntegrityError:
            messages.error(request, 'No se pudo crear la cuenta. Verifica tus datos.')
            return render(request, 'register.html', {'planes': planes})

        login(request, user)
        user.refresh_from_db()
        return render(request, 'register.html', {
            'planes': planes,
            'registro_exitoso': True,
            'usuario': user,
            'plan_elegido': plan,
            'suscripcion': subscription,
        })

    plan_id_get = request.GET.get('plan')
    try:
        plan_seleccionado_id = int(plan_id_get) if plan_id_get else None
    except ValueError:
        plan_seleccionado_id = None

    return render(request, 'register.html', {
        'planes': planes,
        'plan_seleccionado_id': plan_seleccionado_id,
    })

def login_view(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', '').strip()
        password = request.POST.get('password')
        user = authenticate(request, username=rut, password=password)
        if user:
            login(request, user)
            return redirect('landing')
        return render(request, 'login.html', {'error': 'RUT o contraseña incorrectos.'})
    return render(request, 'login.html')

def validar_usuario_ajax(request):
    rut = request.GET.get('rut', '').strip()
    email = request.GET.get('email', '').strip().lower()
    
    errores = []
    if rut and CustomUser.objects.filter(rut=rut).exists():
        errores.append('Ya existe una cuenta con ese RUT.')
    if email and CustomUser.objects.filter(email=email).exists():
        errores.append('Ya existe una cuenta con ese correo electrónico.')
        
    if errores:
        return JsonResponse({'valido': False, 'mensaje': ' '.join(errores)})
    return JsonResponse({'valido': True})