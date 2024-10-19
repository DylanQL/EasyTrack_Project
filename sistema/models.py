from django.db import models
from django.contrib.auth.hashers import make_password


class Cliente(models.Model):
    dni = models.CharField(max_length=15)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Contactanos(models.Model):
    email = models.EmailField()
    nombre = models.CharField(max_length=100)
    asunto = models.CharField(max_length=150)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"

class Terminal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)  # El correo debe ser único para cada empleado
    password = models.CharField(max_length=128)  # Contraseña encriptada

    def save(self, *args, **kwargs):
        # Encriptamos la contraseña antes de guardarla
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Motivo(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion

class Encomienda(models.Model):
    descripcion = models.TextField()
    remitente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="encomiendas_remitente")
    destinatario = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="encomiendas_destinatario")
    placa_vehiculo = models.CharField(max_length=20)
    terminal_partida = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name="terminal_partida")
    terminal_destino = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name="terminal_destino")
    volumen = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_salida = models.DateTimeField(null=True, blank=True)  # Hacerlo opcional
    fecha_llegada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50)
    condicion_envio = models.CharField(max_length=50)
    cantidad_paquetes = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    empleado_registro = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name="empleado_registro")
    empleado_entrega = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name="empleado_entrega", null=True, blank=True)

    def __str__(self):
        return f"Encomienda {self.id} - {self.descripcion}"


class Reclamo(models.Model):
    encomienda = models.ForeignKey(Encomienda, on_delete=models.CASCADE)
    motivo = models.ForeignKey(Motivo, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"Reclamo {self.id} - {self.estado}"

class Comprobante(models.Model):
    encomienda = models.ForeignKey(Encomienda, on_delete=models.CASCADE)
    estado_pago = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField()

    def __str__(self):
        return f"Comprobante {self.id} - {self.estado_pago}"

class Seguridad(models.Model):
    encomienda = models.ForeignKey(Encomienda, on_delete=models.CASCADE)
    clave_habilitada = models.CharField(max_length=128)
    clave_estatica = models.CharField(max_length=128)

    def __str__(self):
        return f"Seguridad para Encomienda {self.encomienda.id}"