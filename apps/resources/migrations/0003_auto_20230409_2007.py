# Generated by Django 3.2.17 on 2023-04-10 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0002_auto_20230407_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='changed_by',
        ),
        migrations.RenameField(
            model_name='historicalcomment',
            old_name='user',
            new_name='changed_by',
        ),
        migrations.AddField(
            model_name='historicaluploadfileform',
            name='changed_by',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='uploadfileform',
            name='changed_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='upload_by', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]