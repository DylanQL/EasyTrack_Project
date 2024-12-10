from django.contrib import admin
from .models import Cliente, Contacto, Terminal, Empleado, Motivo, Encomienda, Reclamo, Comprobante, Seguridad, Vehiculo

# Personalización para Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'apellidos', 'telefono')
    search_fields = ('dni', 'nombres', 'apellidos')

# Personalización para Encomienda
class EncomiendaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'get_remitente_nombres', 'get_destinatario_nombres', 'estado', 'fecha_salida', 'fecha_llegada')
    list_filter = ('estado', 'fecha_salida', 'fecha_llegada')
    search_fields = ('descripcion', 'remitente__nombres', 'destinatario__nombres')

    def get_remitente_nombres(self, obj):
        return f"{obj.remitente.nombres} {obj.remitente.apellidos}"
    get_remitente_nombres.short_description = 'Remitente'

    def get_destinatario_nombres(self, obj):
        return f"{obj.destinatario.nombres} {obj.destinatario.apellidos}"
    get_destinatario_nombres.short_description = 'Destinatario'

# Personalización para Vehículo
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa_vehiculo', 'estado_vehiculo')  # Campos a mostrar en la lista
    search_fields = ('placa_vehiculo',)  # Búsqueda por placa
    list_filter = ('estado_vehiculo',)  # Filtro por estado

# Registrar todos los modelos
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Contacto)
admin.site.register(Terminal)
admin.site.register(Empleado)
admin.site.register(Motivo)
admin.site.register(Encomienda, EncomiendaAdmin)
admin.site.register(Reclamo)
admin.site.register(Comprobante)
admin.site.register(Seguridad)
admin.site.register(Vehiculo, VehiculoAdmin)  # Registrar el modelo Vehículo con personalización