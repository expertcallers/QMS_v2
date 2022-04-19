# Generated by Django 4.0.1 on 2022-01-18 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qms_app', '0007_outbound'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outbound',
            old_name='call_duration_hr',
            new_name='call_duration',
        ),
        migrations.RemoveField(
            model_name='outbound',
            name='call_duration_min',
        ),
        migrations.RemoveField(
            model_name='outbound',
            name='call_duration_sec',
        ),
    ]