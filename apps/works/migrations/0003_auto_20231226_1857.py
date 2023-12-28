# Generated by Django 3.2.17 on 2023-12-27 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0002_auto_20231018_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalwork',
            name='status',
            field=models.CharField(choices=[('nuevo', 'Nuevo'), ('espera', 'En espera'), ('tramite', 'En tramite'), ('concluido', 'Concluido')], default='nuevo', max_length=20, verbose_name='Estado del trabajo'),
        ),
        migrations.AlterField(
            model_name='work',
            name='status',
            field=models.CharField(choices=[('nuevo', 'Nuevo'), ('espera', 'En espera'), ('tramite', 'En tramite'), ('concluido', 'Concluido')], default='nuevo', max_length=20, verbose_name='Estado del trabajo'),
        ),
        migrations.DeleteModel(
            name='HistoricalStatus',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
