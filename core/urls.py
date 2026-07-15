from django.contrib import admin
from django.urls import path, include
from core.views import landing_page
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'),
    
    path('dashboard/', include('dashboard.urls')), 

    path('registrarse/', accounts_views.register, name='register'),
]