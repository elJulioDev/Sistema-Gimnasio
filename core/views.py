from django.shortcuts import render
from plans.models import Plan

def landing_page(request):
    planes = Plan.objects.filter(activo=True)[:3]
    return render(request, 'landing.html', {'planes': planes})