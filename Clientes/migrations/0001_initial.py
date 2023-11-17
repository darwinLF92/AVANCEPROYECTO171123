# Generated by Django 4.2.5 on 2023-11-09 19:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=20, unique=True, verbose_name='NIT')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('direccion', models.CharField(max_length=200, verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=20, verbose_name='Teléfono')),
                ('correo', models.EmailField(max_length=100, verbose_name='Correo Electrónico')),
                ('limitecredito', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Límite de Crédito')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Creación')),
                ('activo', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
    ]