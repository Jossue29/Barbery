from django.urls import path
from . import views  # Solo importamos el views de esta app

urlpatterns = [
    # Gestión usuarios (ADMIN)
    path('', views.users_view, name='users'),
    path('<int:pk>/', views.users_view, name='users_edit'),

    # Mi cuenta (usuario logeado)
    path('mi-cuenta/', views.perfil, name='perfil'),
    path('mi-cuenta/password/', views.cambiar_password, name='cambiar_password'),
]
