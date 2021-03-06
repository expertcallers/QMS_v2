# Generated by Django 4.0.1 on 2022-02-02 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qms_app', '0024_abhindalco_delete_digitalswissgold_delete_emailchat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DigitalSwissGold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(max_length=150)),
                ('campaign_type', models.CharField(default='Digital', max_length=50)),
                ('page_type', models.CharField(default='Digital', max_length=50)),
                ('emp_id', models.CharField(max_length=30)),
                ('associate_name', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=50)),
                ('concept', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_contact', models.CharField(max_length=15)),
                ('call_date', models.DateField()),
                ('call_duration', models.IntegerField(blank=True, null=True)),
                ('audit_date', models.DateField()),
                ('quality_analyst', models.CharField(max_length=100)),
                ('team_lead', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
                ('am', models.CharField(max_length=100)),
                ('team_lead_id', models.CharField(max_length=30)),
                ('manager_id', models.CharField(max_length=30)),
                ('am_id', models.CharField(max_length=30)),
                ('week', models.CharField(max_length=10)),
                ('ce_1', models.IntegerField()),
                ('ce_2', models.IntegerField()),
                ('ce_3', models.IntegerField()),
                ('ce_4', models.IntegerField()),
                ('ce_5', models.IntegerField()),
                ('ce_6', models.IntegerField()),
                ('ce_7', models.IntegerField()),
                ('ce_8', models.IntegerField()),
                ('ce_9', models.IntegerField()),
                ('ce_10', models.IntegerField()),
                ('ce_11', models.IntegerField()),
                ('business_1', models.IntegerField()),
                ('business_2', models.IntegerField()),
                ('compliance_1', models.IntegerField()),
                ('compliance_2', models.IntegerField()),
                ('compliance_3', models.IntegerField()),
                ('compliance_4', models.IntegerField()),
                ('compliance_5', models.IntegerField()),
                ('ce_total', models.IntegerField(null=True)),
                ('business_total', models.IntegerField(null=True)),
                ('compliance_total', models.IntegerField(null=True)),
                ('overall_score', models.IntegerField(null=True)),
                ('areas_improvement', models.TextField()),
                ('positives', models.TextField()),
                ('comments', models.TextField()),
                ('added_by', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('closed_date', models.DateTimeField(null=True)),
                ('emp_comments', models.TextField(null=True)),
                ('fatal', models.BooleanField(default=False)),
                ('fatal_count', models.IntegerField(default=0)),
                ('dispute_status', models.BooleanField(default=False)),
                ('audit_duration', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EmailChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(max_length=150)),
                ('campaign_type', models.CharField(default='Email', max_length=50)),
                ('page_type', models.CharField(default='Email', max_length=50)),
                ('emp_id', models.CharField(max_length=30)),
                ('associate_name', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=50)),
                ('concept', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_contact', models.CharField(max_length=15)),
                ('call_date', models.DateField()),
                ('call_duration', models.IntegerField(blank=True, null=True)),
                ('audit_date', models.DateField()),
                ('quality_analyst', models.CharField(max_length=100)),
                ('team_lead', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
                ('am', models.CharField(max_length=100)),
                ('team_lead_id', models.CharField(max_length=30)),
                ('manager_id', models.CharField(max_length=30)),
                ('am_id', models.CharField(max_length=30)),
                ('week', models.CharField(max_length=10)),
                ('ce_1', models.IntegerField()),
                ('ce_2', models.IntegerField()),
                ('ce_3', models.IntegerField()),
                ('ce_4', models.IntegerField()),
                ('ce_5', models.IntegerField()),
                ('ce_6', models.IntegerField()),
                ('ce_7', models.IntegerField()),
                ('ce_8', models.IntegerField()),
                ('ce_9', models.IntegerField()),
                ('ce_10', models.IntegerField()),
                ('ce_11', models.IntegerField()),
                ('business_1', models.IntegerField()),
                ('business_2', models.IntegerField()),
                ('compliance_1', models.IntegerField()),
                ('compliance_2', models.IntegerField()),
                ('compliance_3', models.IntegerField()),
                ('compliance_4', models.IntegerField()),
                ('compliance_5', models.IntegerField()),
                ('ce_total', models.IntegerField(null=True)),
                ('business_total', models.IntegerField(null=True)),
                ('compliance_total', models.IntegerField(null=True)),
                ('overall_score', models.IntegerField(null=True)),
                ('areas_improvement', models.TextField()),
                ('positives', models.TextField()),
                ('comments', models.TextField()),
                ('added_by', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('closed_date', models.DateTimeField(null=True)),
                ('emp_comments', models.TextField(null=True)),
                ('fatal', models.BooleanField(default=False)),
                ('fatal_count', models.IntegerField(default=0)),
                ('dispute_status', models.BooleanField(default=False)),
                ('audit_duration', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Inbound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(max_length=150)),
                ('campaign_type', models.CharField(default='Inbound', max_length=50)),
                ('page_type', models.CharField(default='Inbound', max_length=50)),
                ('emp_id', models.CharField(max_length=30)),
                ('associate_name', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=50)),
                ('concept', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_contact', models.CharField(max_length=15)),
                ('call_date', models.DateField()),
                ('call_duration', models.IntegerField(blank=True, null=True)),
                ('audit_date', models.DateField()),
                ('quality_analyst', models.CharField(max_length=100)),
                ('team_lead', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
                ('am', models.CharField(max_length=100)),
                ('team_lead_id', models.CharField(max_length=30)),
                ('manager_id', models.CharField(max_length=30)),
                ('am_id', models.CharField(max_length=30)),
                ('week', models.CharField(max_length=10)),
                ('ce_1', models.IntegerField()),
                ('ce_2', models.IntegerField()),
                ('ce_3', models.IntegerField()),
                ('ce_4', models.IntegerField()),
                ('ce_5', models.IntegerField()),
                ('ce_6', models.IntegerField()),
                ('ce_7', models.IntegerField()),
                ('ce_8', models.IntegerField()),
                ('ce_9', models.IntegerField()),
                ('ce_10', models.IntegerField()),
                ('ce_11', models.IntegerField()),
                ('business_1', models.IntegerField()),
                ('business_2', models.IntegerField()),
                ('compliance_1', models.IntegerField()),
                ('compliance_2', models.IntegerField()),
                ('compliance_3', models.IntegerField()),
                ('compliance_4', models.IntegerField()),
                ('compliance_5', models.IntegerField()),
                ('areas_improvement', models.TextField()),
                ('positives', models.TextField()),
                ('comments', models.TextField()),
                ('added_by', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('closed_date', models.DateTimeField(null=True)),
                ('emp_comments', models.TextField(null=True)),
                ('ce_total', models.IntegerField(null=True)),
                ('business_total', models.IntegerField(null=True)),
                ('compliance_total', models.IntegerField(null=True)),
                ('overall_score', models.IntegerField(null=True)),
                ('fatal', models.BooleanField(default=False)),
                ('fatal_count', models.IntegerField(default=0)),
                ('dispute_status', models.BooleanField(default=False)),
                ('audit_duration', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Outbound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(max_length=150)),
                ('campaign_type', models.CharField(default='Outbound', max_length=50)),
                ('page_type', models.CharField(default='Outbound', max_length=50)),
                ('emp_id', models.CharField(max_length=30)),
                ('associate_name', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=50)),
                ('concept', models.CharField(max_length=100)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_contact', models.CharField(max_length=15)),
                ('call_date', models.DateField()),
                ('call_duration', models.IntegerField(blank=True, null=True)),
                ('audit_date', models.DateField()),
                ('quality_analyst', models.CharField(max_length=100)),
                ('team_lead', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
                ('am', models.CharField(max_length=100)),
                ('team_lead_id', models.CharField(max_length=30)),
                ('manager_id', models.CharField(max_length=30)),
                ('am_id', models.CharField(max_length=30)),
                ('week', models.CharField(max_length=10)),
                ('oc_1', models.IntegerField()),
                ('oc_2', models.IntegerField()),
                ('oc_3', models.IntegerField()),
                ('softskill_1', models.IntegerField()),
                ('softskill_2', models.IntegerField()),
                ('softskill_3', models.IntegerField()),
                ('softskill_4', models.IntegerField()),
                ('softskill_5', models.IntegerField()),
                ('compliance_1', models.IntegerField()),
                ('compliance_2', models.IntegerField()),
                ('compliance_3', models.IntegerField()),
                ('compliance_4', models.IntegerField()),
                ('compliance_5', models.IntegerField()),
                ('compliance_6', models.IntegerField()),
                ('areas_improvement', models.TextField()),
                ('positives', models.TextField()),
                ('comments', models.TextField()),
                ('added_by', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('closed_date', models.DateTimeField(null=True)),
                ('emp_comments', models.TextField(null=True)),
                ('oc_total', models.IntegerField(null=True)),
                ('softskill_total', models.IntegerField(null=True)),
                ('compliance_total', models.IntegerField(null=True)),
                ('overall_score', models.IntegerField(null=True)),
                ('fatal', models.BooleanField(default=False)),
                ('fatal_count', models.IntegerField(default=0)),
                ('dispute_status', models.BooleanField(default=False)),
                ('audit_duration', models.TimeField()),
            ],
        ),
    ]
