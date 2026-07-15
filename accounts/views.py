from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import CustomUser  # Asegúrate de importar tu modelo de usuario cuando implementes la lógica

def register(request):
    if request.method == 'POST':
        # Captura de datos del formulario
        rut = request.POST.get('rut')
        nombre = request.POST.get('first_name')
        apellido_paterno = request.POST.get('last_name')
        apellido_materno = request.POST.get('apellido_materno')
        edad = request.POST.get('edad')
        email = request.POST.get('email')
        password = request.POST.get('password')
        plan_seleccionado = request.POST.get('selected_plan')
        
        # ---------------------------------------------------------
        # AQUÍ VA TU LÓGICA DE CREACIÓN DE USUARIO Y VALIDACIÓN
        # Aprovechando tu CustomUser de la app accounts
        # ---------------------------------------------------------
        
        messages.success(request, '¡Registro completado con éxito!')
        return redirect('iniciar_sesion') # Asegúrate de cambiar esto por tu url de login real

    # Petición GET: muestra el formulario
    return render(request, 'register.html')