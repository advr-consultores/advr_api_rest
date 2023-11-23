# Generated by Django 3.2.17 on 2023-11-23 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0011_auto_20231122_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalresource',
            name='detail_state',
            field=models.CharField(choices=[('expectantes', 'En espera del coordinador para indicar la forma de pago.'), ('expectante', 'En espera de recursos por parte del cliente.'), ('aguardando', 'En espera de movimiento por parte del área de cuentas.'), ('comprobacion', 'Comenzando la comprobación del responsable para proceder con la emisión de la factura.'), ('aprobado', 'Confirmación enviada al responsable de que la verificación del trámite es correcta.')], default='expectantes', max_length=244, verbose_name='Detalle del estado'),
        ),
        migrations.AlterField(
            model_name='historicaluploadfileform',
            name='type_file',
            field=models.CharField(choices=[('comprobante', 'Comprobante'), ('factura', 'Factura'), ('acuse', 'Acuse')], default='comprobante', max_length=30, verbose_name='Tipo de documento'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='detail_state',
            field=models.CharField(choices=[('expectantes', 'En espera del coordinador para indicar la forma de pago.'), ('expectante', 'En espera de recursos por parte del cliente.'), ('aguardando', 'En espera de movimiento por parte del área de cuentas.'), ('comprobacion', 'Comenzando la comprobación del responsable para proceder con la emisión de la factura.'), ('aprobado', 'Confirmación enviada al responsable de que la verificación del trámite es correcta.')], default='expectantes', max_length=244, verbose_name='Detalle del estado'),
        ),
        migrations.AlterField(
            model_name='uploadfileform',
            name='type_file',
            field=models.CharField(choices=[('comprobante', 'Comprobante'), ('factura', 'Factura'), ('acuse', 'Acuse')], default='comprobante', max_length=30, verbose_name='Tipo de documento'),
        ),
    ]
