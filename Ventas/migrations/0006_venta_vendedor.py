# Generated by Django 4.2.5 on 2023-11-18 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendedor', '0001_initial'),
        ('Ventas', '0005_alter_venta_cambio_alter_venta_dias_credito_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='vendedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendedor', to='Vendedor.vendedor'),
        ),
    ]
