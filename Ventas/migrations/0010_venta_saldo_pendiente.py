# Generated by Django 4.2.5 on 2023-11-19 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas', '0009_remove_cobro_es_abono_remove_venta_saldo_pendiente'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='saldo_pendiente',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]