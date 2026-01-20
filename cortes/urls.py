from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_cortes, name='cortes_list'),
    path('cortes/editar/<int:corte_id>/', views.editar_corte, name='editar_corte'),

]
