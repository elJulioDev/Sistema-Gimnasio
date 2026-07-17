from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.db import IntegrityError, transaction
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        apellido_materno = request.POST.get('apellido_materno', '').strip()
        edad = request.POST.get('edad') or None
        estudios = request.POST.get('estudios', '').strip()
        email = request.POST.get('email', '').strip().lower()
        telefono = request.POST.get('telefono', '').strip()
        password = request.POST.get('password')
        confirmar_password = request.POST.get('confirmar_password')

        if password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'register.html')

        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'register.html')

        if CustomUser.objects.filter(rut=rut).exists():
            messages.error(request, 'Ya existe una cuenta con ese RUT.')
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe una cuenta con ese correo.')
            return render(request, 'register.html')

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
                    edad=edad,
                    estudios=estudios,
                    telefono=telefono,
                    role=CustomUser.Role.CLIENTE,
                )
        except IntegrityError:
            messages.error(request, 'No se pudo crear la cuenta. Verifica tus datos.')
            return render(request, 'register.html')

        login(request, user)
        messages.success(request, '¡Registro completado con éxito!')
        return redirect('landing')

    return render(request, 'register.html')