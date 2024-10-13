from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Encomienda

# Sistema/views.py

from django.shortcuts import render, redirect
from .models import Cliente

def registro_cliente(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        telefono = request.POST['telefono']

        cliente = Cliente(dni=dni, nombres=nombres, apellidos=apellidos, telefono=telefono)
        cliente.save()

        return redirect('registro_cliente')  # Redirige a la misma página después de registrar

    return render(request, 'registro_cliente.html')