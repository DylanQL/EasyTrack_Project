from django.contrib import admin
from .models import Cliente, Contactanos, Terminal, Empleado, Motivo, Encomienda, Reclamo, Comprobante, Seguridad

# Personalización para Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'apellidos', 'telefono')
    search_fields = ('dni', 'nombres', 'apellidos')

# Personalización para Encomienda
class EncomiendaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'remitente', 'destinatario', 'estado', 'fecha_salida', 'fecha_llegada')
    list_filter = ('estado', 'fecha_salida', 'fecha_llegada')
    search_fields = ('descripcion', 'remitente__nombres', 'destinatario__nombres')

# Registrar todos los modelos
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Contactanos)
admin.site.register(Terminal)
admin.site.register(Empleado)
admin.site.register(Motivo)
admin.site.register(Encomienda, EncomiendaAdmin)
admin.site.register(Reclamo)
admin.site.register(Comprobante)
admin.site.register(Seguridad)
