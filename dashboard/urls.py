from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/', views.admin_dashboard, name='admin_home'),
    path('mi-dashboard/', views.cliente_dashboard, name='cliente_home'),
    path('mi-plan/', views.cliente_plan, name='cliente_plan'),
    path('mi-progreso/', views.cliente_progreso, name='cliente_progreso'),
    path('mi-perfil/', views.cliente_perfil, name='cliente_perfil'),
]