# Generated by Django 5.1.2 on 2024-10-13 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=15)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Contactanos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('nombre', models.CharField(max_length=100)),
                ('asunto', models.CharField(max_length=150)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('ubicacion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Encomienda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('placa_vehiculo', models.CharField(max_length=20)),
                ('volumen', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_salida', models.DateTimeField()),
                ('fecha_llegada', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(max_length=50)),
                ('condicion_envio', models.CharField(max_length=50)),
                ('cantidad_paquetes', models.IntegerField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_entrega', models.DateTimeField(blank=True, null=True)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encomiendas_destinatario', to='sistema.cliente')),
                ('empleado_entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado_entrega', to='sistema.empleado')),
                ('empleado_registro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado_registro', to='sistema.empleado')),
                ('remitente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encomiendas_remitente', to='sistema.cliente')),
                ('terminal_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terminal_destino', to='sistema.terminal')),
                ('terminal_partida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terminal_partida', to='sistema.terminal')),
            ],
        ),
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_pago', models.CharField(max_length=50)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_pago', models.DateTimeField()),
                ('encomienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.encomienda')),
            ],
        ),
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(max_length=50)),
                ('encomienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.encomienda')),
                ('motivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.motivo')),
            ],
        ),
        migrations.CreateModel(
            name='Seguridad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave_habilitada', models.CharField(max_length=128)),
                ('clave_estatica', models.CharField(max_length=128)),
                ('encomienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.encomienda')),
            ],
        ),
    ]
