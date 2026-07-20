from django.contrib import admin
from django.urls import path, include
from core.views import landing_page
from accounts import views as accounts_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'),
    
    path('dashboard/', include('dashboard.urls')), 

    path('registrarse/', accounts_views.register, name='register'),
    path('iniciar-sesion/', accounts_views.login_view, name='login'),
    path('validar-usuario/', accounts_views.validar_usuario_ajax, name='validar_usuario_ajax'),

    path('cerrar-sesion/', LogoutView.as_view(next_page='landing'), name='logout'),
]