from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import IntegrityError, transaction
from datetime import date
from .models import CustomUser
from plans.models import Plan
from django.contrib.auth import login, authenticate

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
            return render(request, 'register.html', {'planes': planes})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe una cuenta con ese correo.')
            return render(request, 'register.html', {'planes': planes})

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