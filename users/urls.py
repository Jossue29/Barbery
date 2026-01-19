from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users_list, name='users_list'),
    path('users/crear/', views.users_create, name='users_create'),
    path('users/<int:pk>/editar/', views.users_update, name='users_update'),
    path('users/<int:pk>/borrar/', views.users_delete, name='users_delete'),
]
