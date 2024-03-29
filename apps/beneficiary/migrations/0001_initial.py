# Generated by Django 3.2.17 on 2023-10-05 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de eliminación')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('interbank_code', models.CharField(max_length=20, verbose_name='Clave interbancaria')),
                ('bank', models.CharField(max_length=50, null=True, verbose_name='Banco')),
            ],
            options={
                'verbose_name': 'Beneficiaro',
                'verbose_name_plural': 'Beneficiaro',
            },
        ),
        migrations.CreateModel(
            name='HistoricalBeneficiary',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(blank=True, editable=False, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(blank=True, editable=False, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(blank=True, editable=False, verbose_name='Fecha de eliminación')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Nombre')),
                ('interbank_code', models.CharField(max_length=20, verbose_name='Clave interbancaria')),
                ('bank', models.CharField(max_length=50, null=True, verbose_name='Banco')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Beneficiaro',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
