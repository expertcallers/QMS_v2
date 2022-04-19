# Generated by Django 4.0.1 on 2022-01-18 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qms_app', '0003_alter_campaign_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mgr', to=settings.AUTH_USER_MODEL),
        ),
    ]