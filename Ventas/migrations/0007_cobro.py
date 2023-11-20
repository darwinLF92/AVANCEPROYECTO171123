# Generated by Django 4.2.5 on 2023-11-19 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendedor', '0001_initial'),
        ('Ventas', '0006_venta_vendedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_cobro', models.DateField(auto_now_add=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('cheque', 'Cheque'), ('transferencia', 'Transferencia')], max_length=13)),
                ('vendedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cobros', to='Vendedor.vendedor')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cobros', to='Ventas.venta')),
            ],
        ),
    ]