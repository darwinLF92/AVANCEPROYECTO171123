# Generated by Django 4.2.5 on 2023-11-09 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
