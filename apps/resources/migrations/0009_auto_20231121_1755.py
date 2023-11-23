# Generated by Django 3.2.17 on 2023-11-21 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_auto_20231121_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalresource',
            name='detail_state',
            field=models.CharField(choices=[('expectantes', 'En espera del coordinador para indicar la forma de pago.'), ('expectante', 'En espera de recursos por parte del cliente.'), ('aguardando', 'En espera de movimiento por parte del área de cuentas.')], default='expectantes', max_length=244, verbose_name='Detalle del estado'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='detail_state',
            field=models.CharField(choices=[('expectantes', 'En espera del coordinador para indicar la forma de pago.'), ('expectante', 'En espera de recursos por parte del cliente.'), ('aguardando', 'En espera de movimiento por parte del área de cuentas.')], default='expectantes', max_length=244, verbose_name='Detalle del estado'),
        ),
    ]
