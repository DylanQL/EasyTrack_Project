from django.contrib import admin
from django.urls import path, include  # Asegúrate de importar include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el administrador de Django
    path('', include('sistema.urls')),   
]