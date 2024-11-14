from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_cliente, name='index_cliente'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contactanos/', views.contactanos, name='contactanos'),
    path('reclamos/', views.reclamos, name='reclamos'),
    path('login-empleado/', views.login_empleado, name='login_empleado'),
    path('registro_cliente/', views.registro_cliente, name='registro_cliente'),
    path('registro_encomienda/', views.registro_encomienda, name='registro_encomienda'),
    path('listado_clientes/', views.listado_clientes, name='listado_clientes'),
    path('listado_reclamos/', views.listado_reclamos, name='listado_reclamos'),
    path('logout/', views.logout_view, name='logout'),  # Ruta para cerrar sesión
    path('panel_empleado/', views.panel_empleado, name='panel_empleado'),
    #path('estado_actualizado/', views.estado_actualizado, name='estado_actualizado'),
    path('actualizar_estado_form/', views.actualizar_estado_form, name='actualizar_estado_form'),
    path('actualizar_estado_form/<int:encomienda_id>/', views.actualizar_estado_form, name='actualizar_estado_form'),
    path('listado_encomiendas/', views.listado_encomiendas, name='listado_encomiendas'),
    path('enviar_reclamo/', views.enviar_reclamo, name='enviar_reclamo'),
    path('encomienda/<int:encomienda_id>/detalles/', views.ver_detalles_encomienda, name='ver_detalles_encomienda'),
    path('seguridad/<int:seguridad_id>/cambiar_estado/', views.cambiar_estado_clave, name='cambiar_estado_clave'),
    path('editar-telefono/<int:cliente_id>/', views.editar_telefono_cliente, name='editar_telefono_cliente'),
    path('control-envios/', views.control_envios, name='control_envios'),

]