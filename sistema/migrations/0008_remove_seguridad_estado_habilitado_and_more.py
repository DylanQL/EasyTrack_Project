# Generated by Django 5.1.2 on 2024-11-10 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0007_seguridad_estado_habilitado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seguridad',
            name='estado_habilitado',
        ),
        migrations.AlterField(
            model_name='seguridad',
            name='clave_habilitada',
            field=models.BooleanField(default=False),
        ),
    ]
