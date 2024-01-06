# Generated by Django 4.2.5 on 2023-12-20 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit_empresa', models.CharField(max_length=20)),
                ('nombre_empresa', models.CharField(max_length=100)),
                ('direccion_empresa', models.CharField(max_length=200)),
                ('telefono_empresa', models.CharField(max_length=20)),
                ('correo_empresa', models.EmailField(blank=True, max_length=254, null=True)),
                ('sitio_web_empresa', models.URLField(blank=True, null=True)),
                ('logo_empresa', models.ImageField(upload_to='logos/')),
                ('fondo_pagina_principal', models.ImageField(blank=True, null=True, upload_to='fondos/')),
            ],
        ),
    ]