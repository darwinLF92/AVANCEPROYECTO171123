# Generated by Django 4.2.5 on 2023-11-25 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas', '0013_devolucion'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobro',
            name='anulado',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='AnulacionCobro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_anulacion', models.DateTimeField(auto_now_add=True)),
                ('razon', models.TextField()),
                ('cobro', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='anulacion_cobro', to='Ventas.cobro')),
            ],
        ),
    ]
