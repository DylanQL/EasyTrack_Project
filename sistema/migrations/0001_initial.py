# Generated by Django 5.1.4 on 2024-12-10 18:40

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
                ('pk_cliente_id', models.AutoField(db_column='pk_cliente_id', primary_key=True, serialize=False)),
                ('dni', models.CharField(max_length=15)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('pk_contacto_id', models.AutoField(db_column='pk_contacto_id', primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255)),
                ('nombre', models.CharField(max_length=100)),
                ('asunto', models.CharField(max_length=150)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'contacto',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('pk_empleado_id', models.AutoField(db_column='pk_empleado_id', primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'empleado',
            },
        ),
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('pk_motivo_id', models.AutoField(db_column='pk_motivo_id', primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'motivo',
            },
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('pk_terminal_id', models.AutoField(db_column='pk_terminal_id', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('ubicacion', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'terminal',
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('pk_vehiculo_id', models.AutoField(db_column='pk_vehiculo_id', primary_key=True, serialize=False)),
                ('placa_vehiculo', models.CharField(max_length=20, unique=True)),
                ('estado_vehiculo', models.CharField(choices=[('Dentro de terminal', 'Dentro de terminal'), ('Fuera de terminal', 'Fuera de terminal')], default='Dentro de terminal', max_length=20)),
            ],
            options={
                'db_table': 'vehiculo',
            },
        ),
        migrations.CreateModel(
            name='Encomienda',
            fields=[
                ('pk_encomienda_id', models.AutoField(db_column='pk_encomienda_id', primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('volumen', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_salida', models.DateTimeField(blank=True, null=True)),
                ('fecha_llegada', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(max_length=50)),
                ('condicion_envio', models.CharField(max_length=50)),
                ('cantidad_paquetes', models.IntegerField()),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_entrega', models.DateTimeField(blank=True, null=True)),
                ('fk_destinatario', models.ForeignKey(db_column='fk_destinatario_id', on_delete=django.db.models.deletion.CASCADE, related_name='encomiendas_destinatario', to='sistema.cliente')),
                ('fk_empleado_entrega', models.ForeignKey(blank=True, db_column='fk_empleado_entrega_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empleado_entrega', to='sistema.empleado')),
                ('fk_empleado_registro', models.ForeignKey(db_column='fk_empleado_registro_id', on_delete=django.db.models.deletion.CASCADE, related_name='empleado_registro', to='sistema.empleado')),
                ('fk_remitente', models.ForeignKey(db_column='fk_remitente_id', on_delete=django.db.models.deletion.CASCADE, related_name='encomiendas_remitente', to='sistema.cliente')),
                ('fk_terminal_destino', models.ForeignKey(db_column='fk_terminal_destino_id', on_delete=django.db.models.deletion.CASCADE, related_name='terminal_destino', to='sistema.terminal')),
                ('fk_terminal_partida', models.ForeignKey(db_column='fk_terminal_partida_id', on_delete=django.db.models.deletion.CASCADE, related_name='terminal_partida', to='sistema.terminal')),
                ('fk_vehiculo', models.ForeignKey(db_column='fk_vehiculo_id', on_delete=django.db.models.deletion.CASCADE, to='sistema.vehiculo')),
            ],
            options={
                'db_table': 'encomienda',
            },
        ),
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('pk_comprobante_id', models.AutoField(db_column='pk_comprobante_id', primary_key=True, serialize=False)),
                ('estado_pago', models.CharField(max_length=50)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_pago', models.DateTimeField(blank=True, null=True)),
                ('fk_encomienda', models.ForeignKey(db_column='fk_encomienda_id', on_delete=django.db.models.deletion.CASCADE, to='sistema.encomienda')),
            ],
            options={
                'db_table': 'comprobante',
            },
        ),
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('pk_reclamo_id', models.AutoField(db_column='pk_reclamo_id', primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(max_length=50)),
                ('fk_encomienda', models.ForeignKey(db_column='fk_encomienda_id', on_delete=django.db.models.deletion.CASCADE, to='sistema.encomienda')),
                ('fk_motivo', models.ForeignKey(db_column='fk_motivo_id', on_delete=django.db.models.deletion.CASCADE, to='sistema.motivo')),
            ],
            options={
                'db_table': 'reclamo',
            },
        ),
        migrations.CreateModel(
            name='Seguridad',
            fields=[
                ('pk_seguridad_id', models.AutoField(db_column='pk_seguridad_id', primary_key=True, serialize=False)),
                ('clave_habilitada', models.BooleanField(default=False)),
                ('clave_estatica', models.CharField(max_length=128)),
                ('fk_encomienda', models.ForeignKey(db_column='fk_encomienda_id', on_delete=django.db.models.deletion.CASCADE, to='sistema.encomienda')),
            ],
            options={
                'db_table': 'seguridad',
            },
        ),
    ]
