# Generated by Django 4.0.1 on 2022-01-25 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qms_app', '0017_fla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fla',
            name='campaign_type',
            field=models.CharField(default='FLA', max_length=50),
        ),
        migrations.AlterField(
            model_name='fla',
            name='page_type',
            field=models.CharField(default='FLA', max_length=50),
        ),
    ]