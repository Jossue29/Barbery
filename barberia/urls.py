from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('users.urls')),
    path('facturacion/', include('facturacion.urls')),
    path('clientes/', include('clientes.urls')),
    path('clientes/', include('clientes.urls')),
    path('cortes/', include('cortes.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
