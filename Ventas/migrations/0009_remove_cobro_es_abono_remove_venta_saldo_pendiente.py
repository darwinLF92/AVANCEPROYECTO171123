# Generated by Django 4.2.5 on 2023-11-19 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas', '0008_cobro_es_abono_venta_saldo_pendiente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cobro',
            name='es_abono',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='saldo_pendiente',
        ),
    ]
