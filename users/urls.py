from django.urls import path
from .views import users_view

urlpatterns = [
    path('users/', users_view, name='users'),
    path('users/<int:pk>/', users_view, name='users_edit'),
]
