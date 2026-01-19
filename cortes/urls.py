from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_cortes, name='cortes_list'),
]
