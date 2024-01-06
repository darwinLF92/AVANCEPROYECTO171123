from django.db import models

class Configuracion(models.Model):
    nit_empresa = models.CharField(max_length=20)
    nombre_empresa = models.CharField(max_length=100)
    direccion_empresa = models.CharField(max_length=200)
    telefono_empresa = models.CharField(max_length=20)
    correo_empresa = models.EmailField(null=True, blank=True)
    sitio_web_empresa = models.URLField(null=True, blank=True)
    logo_empresa = models.ImageField(upload_to='logos/')
    fondo_pagina_principal = models.ImageField(upload_to='fondos/', null=True, blank=True)
