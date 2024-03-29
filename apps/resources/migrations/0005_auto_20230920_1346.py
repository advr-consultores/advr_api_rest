# Generated by Django 3.2.17 on 2023-09-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20230409_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalpetition',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='historicalpetition',
            name='bank_data',
        ),
        migrations.RemoveField(
            model_name='historicalpetition',
            name='beneficiary',
        ),
        migrations.RemoveField(
            model_name='historicalpetition',
            name='method_pay',
        ),
        migrations.RemoveField(
            model_name='historicalresource',
            name='confirm',
        ),
        migrations.RemoveField(
            model_name='historicalresource',
            name='pay_separately',
        ),
        migrations.RemoveField(
            model_name='historicalresource',
            name='type_pay',
        ),
        migrations.RemoveField(
            model_name='petition',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='petition',
            name='bank_data',
        ),
        migrations.RemoveField(
            model_name='petition',
            name='beneficiary',
        ),
        migrations.RemoveField(
            model_name='petition',
            name='method_pay',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='confirm',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='pay_separately',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='type_pay',
        ),
        migrations.AddField(
            model_name='historicalresource',
            name='bank',
            field=models.CharField(max_length=50, null=True, verbose_name='Banco'),
        ),
        migrations.AddField(
            model_name='historicalresource',
            name='beneficiary',
            field=models.CharField(max_length=50, null=True, verbose_name='Beneficiario'),
        ),
        migrations.AddField(
            model_name='historicalresource',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Pagado'),
        ),
        migrations.AddField(
            model_name='historicalresource',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('transferencia', 'Transferencia'), ('cheque', 'Cheque')], max_length=30, verbose_name='Modalidad pago'),
        ),
        migrations.AddField(
            model_name='historicalresource',
            name='transfer_data',
            field=models.TextField(default='{}', verbose_name='Comentario'),
        ),
        migrations.AddField(
            model_name='historicalresource',
            name='transfer_type',
            field=models.CharField(blank=True, choices=[('transferencia', 'Transferencia'), ('cuenta', 'Cuenta'), ('servicio', 'Servicio')], max_length=30, verbose_name='Tipo transferencia'),
        ),
        migrations.AddField(
            model_name='resource',
            name='bank',
            field=models.CharField(max_length=50, null=True, verbose_name='Banco'),
        ),
        migrations.AddField(
            model_name='resource',
            name='beneficiary',
            field=models.CharField(max_length=50, null=True, verbose_name='Beneficiario'),
        ),
        migrations.AddField(
            model_name='resource',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Pagado'),
        ),
        migrations.AddField(
            model_name='resource',
            name='payment_mode',
            field=models.CharField(blank=True, choices=[('transferencia', 'Transferencia'), ('cheque', 'Cheque')], max_length=30, verbose_name='Modalidad pago'),
        ),
        migrations.AddField(
            model_name='resource',
            name='transfer_data',
            field=models.TextField(default='{}', verbose_name='Comentario'),
        ),
        migrations.AddField(
            model_name='resource',
            name='transfer_type',
            field=models.CharField(blank=True, choices=[('transferencia', 'Transferencia'), ('cuenta', 'Cuenta'), ('servicio', 'Servicio')], max_length=30, verbose_name='Tipo transferencia'),
        ),
    ]
