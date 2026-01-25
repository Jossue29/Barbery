# barberia/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .views import home

def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')  # o 'dashboard'
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Raíz: si logueado → dashboard, si no → login
    path('', root_redirect, name='root'),
    
    # Login y logout
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard protegido
    path('home/', home, name='home'),  # o 'dashboard/'
    
    path('users/', include('users.urls')),
    path('facturacion/', include('facturacion.urls')),
    path('clientes/', include('clientes.urls')),
    path('cortes/', include('cortes.urls')),
]