from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from .models import Encomienda, Cliente, Empleado, Reclamo, Motivo, Terminal, Comprobante, Seguridad, Vehiculo, Contacto
from django.contrib.auth import logout
from django.shortcuts import redirect
from django import forms
from .models import Reclamo

import requests  # Importar requests para realizar la llamada a la API

# Decorador para verificar si el empleado está logueado
def empleado_requerido(view_func):
    def wrapper(request, *args, **kwargs):
        if 'empleado_id' not in request.session:
            return redirect('login_empleado')
        return view_func(request, *args, **kwargs)
    return wrapper

# Vista del panel principal del empleado logueado
@empleado_requerido
def panel_empleado(request):
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(pk_empleado_id=empleado_id) if empleado_id else None
    return render(request, 'layout/base_empleado.html', {'empleado': empleado})

# Vista para el listado de clientes
@empleado_requerido
def listado_clientes(request):
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(pk_empleado_id=empleado_id)
    clientes = Cliente.objects.all()
    return render(request, 'listado_clientes.html', {'clientes': clientes, 'empleado': empleado})

# Vista para el listado de encomiendas
@empleado_requerido
def listado_encomiendas(request):
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(pk_empleado_id=empleado_id)
    encomiendas = Encomienda.objects.all()
    return render(request, 'listado_encomiendas.html', {'encomiendas': encomiendas, 'empleado': empleado})

# Vista para el registro de clientes
@empleado_requerido
def registro_cliente(request):
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(pk_empleado_id=empleado_id)
    nombres = ""
    apellidos = ""

    if request.method == "POST":
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')

        # Llamada al API para obtener los nombres y apellidos
        api_url = "https://api.consultasperu.com/api/v1/query"
        api_token = "66fae0c2197c40714c5bf2bc42fe6d2b34cdcd2999abaaa35e929671e87a409a"
        payload = {
            "token": api_token,
            "type_document": "dni",
            "document_number": dni
        }

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200 and response.json().get('success'):
                data = response.json().get('data', {})
                nombres = data.get('name', '')
                apellidos = data.get('surname', '')
            else:
                messages.error(request, f"Error al obtener datos del DNI: {response.json().get('message')}")
                return render(request, 'registro_cliente.html', {'empleado': empleado})
        except Exception as e:
            messages.error(request, f"Error en la comunicación con la API: {str(e)}")
            return render(request, 'registro_cliente.html', {'empleado': empleado})

        # Crear un nuevo cliente en la base de datos
        nuevo_cliente = Cliente(dni=dni, nombres=nombres, apellidos=apellidos, telefono=telefono)
        nuevo_cliente.save()
        messages.success(request, "Cliente registrado con éxito.")
        return redirect('listado_clientes')

    return render(request, 'registro_cliente.html', {'empleado': empleado})



@empleado_requerido
def registro_encomienda(request):
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(pk_empleado_id=empleado_id)
    terminales = Terminal.objects.all()
    vehiculos = Vehiculo.objects.all()
    CONDICIONES_ENVIO = [
        ('fragil', 'Frágil'),
        ('normal', 'Normal'),
        ('perecedero', 'Perecedero'),
    ]

    if request.method == "POST":
        # Obtener datos del formulario
        remitente_dni = request.POST.get('remitente')
        destinatario_dni = request.POST.get('destinatario')

        try:
            remitente = Cliente.objects.get(dni=remitente_dni)
        except Cliente.DoesNotExist:
            messages.error(request, f"Remitente con DNI {remitente_dni} no registrado.")
            return redirect('registro_encomienda')

        try:
            destinatario = Cliente.objects.get(dni=destinatario_dni)
        except Cliente.DoesNotExist:
            messages.error(request, f"Destinatario con DNI {destinatario_dni} no registrado.")
            return redirect('registro_encomienda')

        vehiculo_id = request.POST.get('vehiculo')
        terminal_partida_id = request.POST.get('terminal_partida')
        terminal_destino_id = request.POST.get('terminal_destino')
        descripcion = request.POST.get('descripcion')
        volumen = request.POST.get('volumen')
        estado_pago = request.POST.get('estado_pago')
        condicion_envio = request.POST.get('condicion_envio')
        clave_estatica = request.POST.get('clave_estatica')
        cantidad_paquetes = request.POST.get('cantidad_paquetes')

        # Validar que todos los campos requeridos estén presentes y sean válidos
        if not (vehiculo_id and terminal_partida_id and terminal_destino_id and descripcion and volumen and estado_pago and condicion_envio and clave_estatica and cantidad_paquetes):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('registro_encomienda')

        try:
            volumen = float(volumen)
            cantidad_paquetes = int(cantidad_paquetes)
        except (ValueError, TypeError):
            messages.error(request, "Volumen y cantidad de paquetes deben ser números válidos.")
            return redirect('registro_encomienda')

        monto = volumen * 2.5

        # Crear y guardar la encomienda
        encomienda = Encomienda.objects.create(
            descripcion=descripcion,
            fk_remitente=remitente,
            fk_destinatario=destinatario,
            fk_vehiculo=Vehiculo.objects.get(pk_vehiculo_id=vehiculo_id),
            fk_terminal_partida=Terminal.objects.get(pk_terminal_id=terminal_partida_id),
            fk_terminal_destino=Terminal.objects.get(pk_terminal_id=terminal_destino_id),
            volumen=volumen,
            estado="No entregado",
            condicion_envio=condicion_envio,
            cantidad_paquetes=cantidad_paquetes,
            fk_empleado_registro=empleado,
            fecha_registro=timezone.now(),
        )

        # Crear y guardar el comprobante de pago
        Comprobante.objects.create(
            fk_encomienda=encomienda,
            estado_pago=estado_pago,
            monto=monto,
            fecha_pago=timezone.now() if estado_pago == 'Pagado' else None
        )

        # Crear y guardar la información de seguridad
        Seguridad.objects.create(
            fk_encomienda=encomienda,
            clave_habilitada=False,
            clave_estatica=clave_estatica
        )

        messages.success(request, "Encomienda registrada con éxito.")
        return redirect('listado_encomiendas')

    return render(request, 'registro_encomienda.html', {
        'terminales': terminales,
        'vehiculos': vehiculos,
        'condiciones_envio': CONDICIONES_ENVIO,
        'empleado': empleado,
    })

# Vista para el listado de reclamos
@empleado_requerido
def listado_reclamos(request):
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(pk_empleado_id=empleado_id)
    reclamos = Reclamo.objects.all()
    return render(request, 'listado_reclamos.html', {'reclamos': reclamos, 'empleado': empleado})

# Vista para cerrar la sesión del empleado
@empleado_requerido
def logout_view(request):
    logout(request)
    return redirect('login_empleado')

# Vista para la página principal del cliente
def index_cliente(request):
    return render(request, 'index_cliente.html')

# Vista para la sección "Nosotros"
def nosotros(request):
    return render(request, 'nosotros.html')

# Vista para la sección "Contáctanos"
def contactanos(request):
    return render(request, 'contactanos.html')

# Vista para el formulario de reclamos
def reclamos(request):
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        descripcion = request.POST.get('descripcion')
        nuevo_reclamo = Reclamo(motivo=motivo, descripcion=descripcion)
        nuevo_reclamo.save()
        messages.success(request, 'Reclamo enviado con éxito.')
        return redirect('reclamos')
    return render(request, 'reclamos.html')

# Vista de inicio de sesión para el empleado
def login_empleado(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        password = request.POST.get('password')
        try:
            empleado = Empleado.objects.get(correo=email)
            if check_password(password, empleado.password):
                request.session['empleado_id'] = empleado.pk_empleado_id  # Usar pk_empleado_id
                messages.success(request, 'Sesión iniciada con éxito')
                return redirect('panel_empleado')
            else:
                messages.error(request, 'Correo o contraseña incorrectos')
        except Empleado.DoesNotExist:
            messages.error(request, 'El correo ingresado no pertenece a ningún empleado registrado.')
    return render(request, 'login_empleado.html')

@empleado_requerido
def editar_telefono_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk_cliente_id=cliente_id)  # Usar pk_cliente_id
    
    if request.method == "POST":
        nuevo_telefono = request.POST.get("telefono")
        cliente.telefono = nuevo_telefono
        cliente.save()
        messages.success(request, "Número de teléfono actualizado con éxito.")
        return redirect('listado_clientes')

    return render(request, 'editar_telefono_cliente.html', {'cliente': cliente})

@empleado_requerido
def control_envios(request):
    vehiculos = Vehiculo.objects.all()
    empleado_id = request.session.get('empleado_id')
    empleado = Empleado.objects.get(pk_empleado_id=empleado_id)

    if request.method == "POST":
        vehiculo_id = request.POST.get("vehiculo")
        vehiculo = get_object_or_404(Vehiculo, pk_vehiculo_id=vehiculo_id)  # Usar pk_vehiculo_id en lugar de id

        # Verificar el estado del vehículo para realizar la acción correspondiente
        if vehiculo.estado_vehiculo == "Dentro de terminal":
            # Cambiar el estado del vehículo a "Fuera de terminal"
            vehiculo.estado_vehiculo = "Fuera de terminal"

            # Actualizar únicamente las encomiendas con fecha_salida en null
            Encomienda.objects.filter(fk_vehiculo=vehiculo, fecha_salida__isnull=True).update(fecha_salida=timezone.now())  # Usar fk_vehiculo en lugar de vehiculo

        elif vehiculo.estado_vehiculo == "Fuera de terminal":
            # Cambiar el estado del vehículo a "Dentro de terminal"
            vehiculo.estado_vehiculo = "Dentro de terminal"

            # Actualizar únicamente las encomiendas con:
            # - fecha_llegada en null
            # - fecha_salida no en null
            Encomienda.objects.filter(
                fk_vehiculo=vehiculo,  # Usar fk_vehiculo en lugar de vehiculo
                fecha_llegada__isnull=True,
                fecha_salida__isnull=False
            ).update(fecha_llegada=timezone.now())

        vehiculo.save()
        messages.success(request, "El estado del vehículo y las encomiendas asociadas han sido actualizados correctamente.")

    return render(request, 'control_envios.html', {
        'vehiculos': vehiculos,
        'empleado': empleado,  
    })

@empleado_requerido
def actualizar_estado_form(request, encomienda_id=None):
    encomienda = None
    comprobante = None
    monto = None

    # Recupera el empleado logueado
    empleado_id = request.session.get('empleado_id')
    empleado = None
    if empleado_id:
        empleado = Empleado.objects.get(pk_empleado_id=empleado_id)

    if encomienda_id:
        encomienda = get_object_or_404(Encomienda, pk_encomienda_id=encomienda_id)  # Usar pk_encomienda_id en lugar de id
        comprobante = Comprobante.objects.filter(fk_encomienda=encomienda).first()  # Usar fk_encomienda en lugar de encomienda
        monto = comprobante.monto if comprobante else 'Error'
    
    if request.method == 'POST' and encomienda:
        # Obtener el estado de pago del formulario
        nuevo_estado_pago = request.POST.get('estado_pago')

        if comprobante:
            comprobante.estado_pago = nuevo_estado_pago
            # Si el estado de pago es "Pagado", actualizamos la fecha de pago
            if nuevo_estado_pago == "Pagado":
                comprobante.fecha_pago = timezone.now()
            comprobante.save()
        
        # Mensaje de éxito y redirección al listado de encomiendas
        messages.success(request, 'El estado de pago se actualizó de manera exitosa.')
        return redirect('listado_encomiendas')  # Redirige a la lista de encomiendas o página adecuada

    return render(request, 'actualizar_estado_form.html', {
        'encomienda': encomienda,
        'comprobante': comprobante,
        'monto': monto,
        'empleado': empleado,
    })

class ReclamoForm(forms.Form):
    encomienda_id = forms.CharField(
        max_length=10,
        label="ID de la Encomienda",
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa el ID del pedido'}),
    )
    motivo = forms.ModelChoiceField(
        queryset=Motivo.objects.all(),  # Mostrar todos los motivos disponibles
        label="Motivo del Reclamo",
        empty_label="Selecciona un motivo",
    )
    descripcion = forms.CharField(
        label="Descripción del Reclamo",
        widget=forms.Textarea(attrs={'placeholder': 'Describe tu reclamo...'}),
    )

from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Encomienda, Motivo, Reclamo

class ReclamoForm(forms.Form):
    encomienda_id = forms.CharField(
        max_length=10,
        label="ID de la Encomienda",
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa el ID del pedido'}),
    )
    motivo = forms.ModelChoiceField(
        queryset=Motivo.objects.all(),  # Mostrar todos los motivos disponibles
        label="Motivo del Reclamo",
        empty_label="Selecciona un motivo",
    )
    descripcion = forms.CharField(
        label="Descripción del Reclamo",
        widget=forms.Textarea(attrs={'placeholder': 'Describe tu reclamo...'}),
    )

def enviar_reclamo(request):
    if request.method == 'POST':
        form = ReclamoForm(request.POST)
        if form.is_valid():
            encomienda_id = form.cleaned_data['encomienda_id']
            motivo = form.cleaned_data['motivo']  # Obtener el objeto Motivo seleccionado
            descripcion = form.cleaned_data['descripcion']
            
            try:
                # Verificar si la encomienda existe
                encomienda = Encomienda.objects.get(pk_encomienda_id=encomienda_id)  # Usar pk_encomienda_id en lugar de id
                
                # Crear el reclamo
                Reclamo.objects.create(
                    fk_encomienda=encomienda,  # Usar fk_encomienda en lugar de encomienda
                    fk_motivo=motivo,  # Usar el objeto Motivo directamente
                    descripcion=descripcion,
                    estado='Pendiente'
                )
                
                messages.success(request, 'Tu reclamo ha sido enviado exitosamente.')
                return redirect('enviar_reclamo')  # Redirige a la misma página o a una página de confirmación
            
            except Encomienda.DoesNotExist:
                messages.error(request, f"No se encontró una encomienda con ID {encomienda_id}.")
    
    else:
        form = ReclamoForm()
    
    return render(request, 'reclamos.html', {'form': form})

def contactanos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        # Guardar el mensaje en la base de datos
        Contacto.objects.create(  # Actualizado
            nombre=nombre,
            email=email,
            asunto=asunto,
            mensaje=mensaje,
            fecha=timezone.now()
        )

        # Mensaje de éxito
        messages.success(request, 'Tu mensaje ha sido enviado correctamente.')
        return redirect('contactanos')  # Redirigir a la misma página después de enviar

    return render(request, 'contactanos.html')

def ver_detalles_encomienda(request, encomienda_id):
    # Recupera el objeto Encomienda
    encomienda = get_object_or_404(Encomienda, pk_encomienda_id=encomienda_id)  # Usar pk_encomienda_id en lugar de id
    
    # Recupera el empleado logueado
    empleado_id = request.session.get('empleado_id')
    empleado = None
    if empleado_id:
        empleado = Empleado.objects.get(pk_empleado_id=empleado_id)
    
    # Recupera los objetos relacionados
    comprobante = Comprobante.objects.filter(fk_encomienda=encomienda).first()  # Usar fk_encomienda en lugar de encomienda
    seguridad = Seguridad.objects.filter(fk_encomienda=encomienda).first()  # Usar fk_encomienda en lugar de encomienda
    reclamos = Reclamo.objects.filter(fk_encomienda=encomienda)  # Usar fk_encomienda en lugar de encomienda
    
    # Pasa estos objetos al template
    context = {
        'encomienda': encomienda,
        'comprobante': comprobante,
        'seguridad': seguridad,
        'reclamos': reclamos,
        'empleado': empleado,  # Pasar el empleado al template
    }
    return render(request, 'detalles_listado_encomienda.html', context)


@empleado_requerido
def cambiar_estado_clave(request, seguridad_id):
    seguridad = get_object_or_404(Seguridad, pk_seguridad_id=seguridad_id)  # Usar pk_seguridad_id en lugar de id
    encomienda = seguridad.fk_encomienda  # Obtener la encomienda asociada
    
    # Alternar el estado de la clave
    seguridad.clave_habilitada = not seguridad.clave_habilitada
    seguridad.save()
    
    # Actualizar el campo empleado_entrega en la encomienda
    empleado_id = request.session.get('empleado_id')
    if empleado_id:
        empleado = Empleado.objects.get(pk_empleado_id=empleado_id)
        encomienda.fk_empleado_entrega = empleado  # Registrar el empleado actual como quien hizo el cambio
        encomienda.save()
    
    messages.success(request, "El estado de la clave y el empleado que realizó el cambio se han actualizado correctamente.")
    return redirect('ver_detalles_encomienda', encomienda_id=encomienda.pk_encomienda_id)  # Usar pk_encomienda_id en lugar de id


def index_cliente(request):
    encomienda_id = request.GET.get('encomienda_id')  # Obtener el ID de encomienda ingresado
    encomienda = None
    estados = []

    if encomienda_id:
        try:
            # Buscar la encomienda usando el campo pk_encomienda_id
            encomienda = Encomienda.objects.get(pk_encomienda_id=int(encomienda_id))
            
            # Lista de estados con fechas correspondientes
            estados = [
                ("Encomienda en terminal", encomienda.fecha_registro),
                ("Encomienda salió de terminal", encomienda.fecha_salida),
                ("Encomienda llegó a terminal destino", encomienda.fecha_llegada),
                ("Encomienda lista para recoger", encomienda.fecha_llegada),
                ("Encomienda entregada", encomienda.fecha_entrega),
            ]
        except (Encomienda.DoesNotExist, ValueError):
            encomienda = None  # No se encontró la encomienda o el ID no es válido

    return render(request, 'index_cliente.html', {
        'encomienda': encomienda,
        'estados': estados,
        'encomienda_id': encomienda_id,
    })


# views.py
from django.shortcuts import render
from django.utils import timezone  # Importa timezone para obtener la fecha y hora actual
from .models import Encomienda, Seguridad

def entrega_paquete(request):
    message = None
    if request.method == 'POST':
        id_encomienda = request.POST.get('id_encomienda')
        clave = request.POST.get('clave')

        try:
            encomienda = Encomienda.objects.get(pk_encomienda_id=id_encomienda)
            seguridad = Seguridad.objects.get(fk_encomienda=encomienda)
        except Encomienda.DoesNotExist:
            message = 'ID de encomienda no existe.'
            return render(request, 'validacion_contraseña.html', {'message': message})
        except Seguridad.DoesNotExist:
            message = 'No se encontró información de seguridad para esta encomienda.'
            return render(request, 'validacion_contraseña.html', {'message': message})

        if seguridad.clave_habilitada:
            if seguridad.clave_estatica == clave:
                # Actualiza el estado de la encomienda y la fecha de entrega
                encomienda.estado = 'Entregado'
                encomienda.fecha_entrega = timezone.now()  # Establece la fecha y hora actual
                encomienda.save()
                message = 'Contraseña aceptada correctamente. Encomienda marcada como entregada.'
            else:
                message = 'Contraseña incorrecta.'
        else:
            message = 'Contraseña no habilitada.'

    return render(request, 'validacion_contraseña.html', {'message': message})