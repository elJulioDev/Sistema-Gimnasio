from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'dashboard/admin_home.html')