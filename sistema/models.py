from django.db import models
from django.contrib.auth.hashers import make_password

class Cliente(models.Model):
    pk_cliente_id = models.AutoField(primary_key=True, db_column='pk_cliente_id')
    dni = models.CharField(max_length=15, null=False, blank=False)
    nombres = models.CharField(max_length=100, null=False, blank=False)
    apellidos = models.CharField(max_length=100, null=False, blank=False)
    telefono = models.CharField(max_length=15, null=True, blank=True)  # Puede ser NULL según MySQL

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        db_table = 'cliente'


class Contacto(models.Model):  # Renombrado de Contactanos a Contacto para coincidir con MySQL
    pk_contacto_id = models.AutoField(primary_key=True, db_column='pk_contacto_id')
    email = models.EmailField(max_length=255, null=False, blank=False)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    asunto = models.CharField(max_length=150, null=False, blank=False)
    mensaje = models.TextField(null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"

    class Meta:
        db_table = 'contacto'  # Aseguramos que el nombre de la tabla coincida con MySQL


class Terminal(models.Model):
    pk_terminal_id = models.AutoField(primary_key=True, db_column='pk_terminal_id')
    nombre = models.CharField(max_length=100, null=False, blank=False)
    direccion = models.CharField(max_length=200, null=False, blank=False)
    ubicacion = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'terminal'


class Empleado(models.Model):
    pk_empleado_id = models.AutoField(primary_key=True, db_column='pk_empleado_id')
    nombres = models.CharField(max_length=100, null=False, blank=False)
    apellidos = models.CharField(max_length=100, null=False, blank=False)
    correo = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)

    def save(self, *args, **kwargs):
        # Encriptamos la contraseña antes de guardarla
        if not self.pk:  # Solo en creación
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        db_table = 'empleado'


class Motivo(models.Model):
    pk_motivo_id = models.AutoField(primary_key=True, db_column='pk_motivo_id')
    descripcion = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        db_table = 'motivo'


class Vehiculo(models.Model):
    pk_vehiculo_id = models.AutoField(primary_key=True, db_column='pk_vehiculo_id')
    placa_vehiculo = models.CharField(max_length=20, unique=True, null=False, blank=False)
    ESTADO_CHOICES = [
        ('Dentro de terminal', 'Dentro de terminal'),
        ('Fuera de terminal', 'Fuera de terminal'),
    ]
    estado_vehiculo = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Dentro de terminal',
        null=False,
        blank=False
    )

    def __str__(self):
        return f"{self.placa_vehiculo} - {self.estado_vehiculo}"

    class Meta:
        db_table = 'vehiculo'


class Encomienda(models.Model):
    pk_encomienda_id = models.AutoField(primary_key=True, db_column='pk_encomienda_id')
    descripcion = models.TextField(null=False, blank=False)
    fk_remitente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="encomiendas_remitente",
        db_column='fk_remitente_id'
    )
    fk_destinatario = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="encomiendas_destinatario",
        db_column='fk_destinatario_id'
    )
    fk_vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        db_column='fk_vehiculo_id'
    )
    fk_terminal_partida = models.ForeignKey(
        Terminal,
        on_delete=models.CASCADE,
        related_name="terminal_partida",
        db_column='fk_terminal_partida_id'
    )
    fk_terminal_destino = models.ForeignKey(
        Terminal,
        on_delete=models.CASCADE,
        related_name="terminal_destino",
        db_column='fk_terminal_destino_id'
    )
    volumen = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    fecha_llegada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50, null=False, blank=False)
    condicion_envio = models.CharField(max_length=50, null=False, blank=False)
    cantidad_paquetes = models.IntegerField(null=False, blank=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    fk_empleado_registro = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name="empleado_registro",
        db_column='fk_empleado_registro_id'
    )
    fk_empleado_entrega = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name="empleado_entrega",
        db_column='fk_empleado_entrega_id',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Encomienda {self.pk_encomienda_id} - {self.descripcion}"

    class Meta:
        db_table = 'encomienda'


class Reclamo(models.Model):
    pk_reclamo_id = models.AutoField(primary_key=True, db_column='pk_reclamo_id')
    fk_encomienda = models.ForeignKey(
        Encomienda,
        on_delete=models.CASCADE,
        db_column='fk_encomienda_id'
    )
    fk_motivo = models.ForeignKey(
        Motivo,
        on_delete=models.CASCADE,
        db_column='fk_motivo_id'
    )
    descripcion = models.TextField(null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"Reclamo {self.pk_reclamo_id} - {self.estado}"

    class Meta:
        db_table = 'reclamo'


class Comprobante(models.Model):
    pk_comprobante_id = models.AutoField(primary_key=True, db_column='pk_comprobante_id')
    fk_encomienda = models.ForeignKey(
        Encomienda,
        on_delete=models.CASCADE,
        db_column='fk_encomienda_id'
    )
    estado_pago = models.CharField(max_length=50, null=False, blank=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Comprobante {self.pk_comprobante_id} - {self.estado_pago}"

    class Meta:
        db_table = 'comprobante'


class Seguridad(models.Model):
    pk_seguridad_id = models.AutoField(primary_key=True, db_column='pk_seguridad_id')
    fk_encomienda = models.ForeignKey(
        Encomienda,
        on_delete=models.CASCADE,
        db_column='fk_encomienda_id'
    )
    clave_habilitada = models.BooleanField(default=False, null=False, blank=False)
    clave_estatica = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f"Seguridad para Encomienda {self.fk_encomienda.pk_encomienda_id}"

    class Meta:
        db_table = 'seguridad'
