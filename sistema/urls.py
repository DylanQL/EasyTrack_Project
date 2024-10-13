# Sistema/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('registro_cliente/', views.registro_cliente, name='registro_cliente'),
    # Agrega más URLs según sea necesario
]