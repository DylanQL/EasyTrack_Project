from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Encomienda, Cliente, Empleado, Reclamo, Motivo, Terminal
from django.utils import timezone


User = get_user_model()

# Vista de la página principal del cliente
def index_cliente(request):
    return render(request, 'index_cliente.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contactanos(request):
    return render(request, 'contactanos.html')

def reclamos(request):
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        descripcion = request.POST.get('descripcion')

        nuevo_reclamo = Reclamo(motivo=motivo, descripcion=descripcion)
        nuevo_reclamo.save()

        messages.success(request, 'Reclamo enviado con éxito.')
        return redirect('reclamos')

    return render(request, 'reclamos.html')


def login_empleado(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            empleado = Empleado.objects.get(correo=email)

            if check_password(password, empleado.password):
                request.session['empleado_id'] = empleado.id
                messages.success(request, 'Sesión iniciada con éxito')
                return redirect('panel_empleado')  # Redirige al panel del empleado
            else:
                messages.error(request, 'Correo o contraseña incorrectos')
        except Empleado.DoesNotExist:
            messages.error(request, 'El correo ingresado no pertenece a ningún empleado registrado.')

    return render(request, 'login_empleado.html')


def empleado_requerido(view_func):
    def wrapper(request, *args, **kwargs):
        if 'empleado_id' not in request.session:
            return redirect('login_empleado')
        return view_func(request, *args, **kwargs)
    return wrapper


@empleado_requerido
def panel_empleado(request):
    empleado_id = request.session.get('empleado_id')
    if empleado_id:
        empleado = Empleado.objects.get(id=empleado_id)
    else:
        empleado = None

    return render(request, 'layout/base_empleado.html', {'empleado': empleado})


@empleado_requerido
def registro_cliente(request):
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(id=empleado_id)

    if request.method == "POST":
        dni = request.POST.get('dni')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')

        nuevo_cliente = Cliente(dni=dni, nombres=nombres, apellidos=apellidos, telefono=telefono)
        nuevo_cliente.save()

        return redirect('listado_clientes')

    return render(request, 'registro_cliente.html', {'empleado': empleado})
@empleado_requerido
def registro_encomienda(request):
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(id=empleado_id)  # Empleado que registra

    # Obtener las terminales para mostrarlas como opciones en el formulario
    terminales = Terminal.objects.all()

    # Definir las opciones para la condición de envío
    CONDICIONES_ENVIO = [
        ('fragil', 'Frágil'),
        ('normal', 'Normal'),
        ('perecedero', 'Perecedero'),
    ]

    if request.method == "POST":
        descripcion = request.POST.get('descripcion')
        remitente = request.POST.get('remitente')
        destinatario = request.POST.get('destinatario')
        placa_vehiculo = request.POST.get('placa_vehiculo')
        terminal_partida_id = request.POST.get('terminal_partida')
        terminal_destino_id = request.POST.get('terminal_destino')
        volumen = request.POST.get('volumen')
        estado = request.POST.get('estado')
        condicion_envio = request.POST.get('condicion_envio')
        cantidad_paquetes = request.POST.get('cantidad_paquetes')

        # Obtener los objetos relacionados
        remitente_obj = Cliente.objects.get(id=remitente)
        destinatario_obj = Cliente.objects.get(id=destinatario)
        terminal_partida_obj = Terminal.objects.get(id=terminal_partida_id)
        terminal_destino_obj = Terminal.objects.get(id=terminal_destino_id)

        # Asignar la fecha actual a 'fecha_salida'
        fecha_salida = timezone.now()

        # Crear la nueva encomienda y asignar empleado_entrega y empleado_registro
        nueva_encomienda = Encomienda(
            descripcion=descripcion,
            remitente=remitente_obj,
            destinatario=destinatario_obj,
            placa_vehiculo=placa_vehiculo,
            terminal_partida=terminal_partida_obj,
            terminal_destino=terminal_destino_obj,
            volumen=volumen,
            estado=estado,
            condicion_envio=condicion_envio,
            cantidad_paquetes=cantidad_paquetes,
            fecha_salida=fecha_salida,
            empleado_registro=empleado,  # Asignar empleado que registra la encomienda
            empleado_entrega=empleado  # Asignar el mismo empleado como entregador por ahora
        )
        nueva_encomienda.save()

        messages.success(request, 'Encomienda registrada con éxito.')


        messages.success(request, 'Encomienda registrada con éxito.')
        return redirect('listado_encomiendas')

    return render(request, 'registro_encomienda.html', {'empleado': empleado, 'terminales': terminales, 'condiciones_envio': CONDICIONES_ENVIO})
@empleado_requerido
def listado_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listado_clientes.html', {'clientes': clientes})


@empleado_requerido
def listado_encomiendas(request):
    encomiendas = Encomienda.objects.all()
    return render(request, 'listado_encomiendas.html', {'encomiendas': encomiendas})


@empleado_requerido
def listado_reclamos(request):
    reclamos = Reclamo.objects.all()
    return render(request, 'listado_reclamos.html', {'reclamos': reclamos})


@empleado_requerido
def actualizar_estado_encomienda(request, encomienda_id=None):
    encomienda = get_object_or_404(Encomienda, id=encomienda_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        encomienda.estado = nuevo_estado
        encomienda.save()
        messages.success(request, 'Estado de la encomienda actualizado con éxito.')
        return redirect('listado_encomiendas')

    return render(request, 'actualizar_estado_encomienda.html', {'encomienda': encomienda})


@empleado_requerido
def logout_view(request):
    logout(request)
    return redirect('login_empleado')
