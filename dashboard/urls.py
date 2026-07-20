from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/', views.admin_dashboard, name='admin_home'),
    path('mi-dashboard/', views.cliente_dashboard, name='cliente_home'),
]