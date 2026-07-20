from django.shortcuts import render
from accounts.decorators import role_required
from accounts.models import CustomUser

@role_required(CustomUser.Role.ADMIN)
def admin_dashboard(request):
    return render(request, 'dashboard/admin_home.html')

@role_required(CustomUser.Role.CLIENTE)
def cliente_dashboard(request):
    return render(request, 'dashboard/cliente_home.html')