from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=30, unique=True)
    emp_name = models.CharField(max_length=100)
    emp_desi = models.CharField(max_length=100)
    emp_process = models.CharField(max_length=150)
    emp_rm1 = models.CharField(max_length=100)
    emp_rm1_id = models.CharField(max_length=30)
    emp_rm2 = models.CharField(max_length=100)
    emp_rm2_id = models.CharField(max_length=30)
    emp_rm3 = models.CharField(max_length=100)
    emp_rm3_id = models.CharField(max_length=30)
    agent_status = models.CharField(max_length=100, default='Active')
    emp_email = models.EmailField(null=True, blank=True)
    pc = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=30, null=True, blank=True)
    email_verify = models.BooleanField(default=False)

    def __str__(self):
        return self.emp_name


class Campaign(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=50)
    campaign_type = models.CharField(max_length=150, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(max_length=50)
    threshold = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class CampaignMapping(models.Model):
    qa = models.CharField(max_length=150)
    qa_id = models.CharField(max_length=50)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)


class AuditIdTable(models.Model):
    audit_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.audit_id)


class Outbound(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Outbound', max_length=50)
    type = models.CharField(default='Outbound', max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Outbound', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)

    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # Opening and Closing
    oc_1 = models.IntegerField()
    oc_2 = models.IntegerField()
    oc_3 = models.IntegerField()
    # SoftSkills
    softskill_1 = models.IntegerField()
    softskill_2 = models.IntegerField()
    softskill_3 = models.IntegerField()
    softskill_4 = models.IntegerField()
    softskill_5 = models.IntegerField()
    # Business and Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()
    compliance_6 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    oc_total = models.IntegerField(null=True)
    softskill_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class Inbound(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Inbound', max_length=50)
    type = models.CharField(default='Inbound', max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Inbound', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    # Customer Experience
    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()
    ce_5 = models.IntegerField()
    ce_6 = models.IntegerField()
    ce_7 = models.IntegerField()
    ce_8 = models.IntegerField()
    ce_9 = models.IntegerField()
    ce_10 = models.IntegerField()
    ce_11 = models.IntegerField()

    # Business
    business_1 = models.IntegerField()
    business_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    ce_total = models.IntegerField(null=True)
    business_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class EmailChat(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Email / Chat', max_length=50)
    type = models.CharField(default='Email / Chat', max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Email', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # questions
    # Customer Experience

    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()
    ce_5 = models.IntegerField()
    ce_6 = models.IntegerField()
    ce_7 = models.IntegerField()
    ce_8 = models.IntegerField()
    ce_9 = models.IntegerField()
    ce_10 = models.IntegerField()
    ce_11 = models.IntegerField()

    # Business
    business_1 = models.IntegerField()
    business_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()

    # Scores
    ce_total = models.IntegerField(null=True)
    business_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class DigitalSwissGold(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Digital', max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Digital', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # questions
    # Customer Experience

    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()
    ce_5 = models.IntegerField()
    ce_6 = models.IntegerField()
    ce_7 = models.IntegerField()
    ce_8 = models.IntegerField()
    ce_9 = models.IntegerField()
    ce_10 = models.IntegerField()
    ce_11 = models.IntegerField()

    # Business
    business_1 = models.IntegerField()
    business_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()

    # Scores
    ce_total = models.IntegerField(null=True)
    business_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class FLA(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='FLA', max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='FLA', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    transaction_handles_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    service = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)

    # questions
    check_list = models.IntegerField()

    # Scores
    overall_score = models.IntegerField(null=True)

    reason_for_failure = models.TextField()
    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class BlazingHog(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='BlazingHog', max_length=50)
    type = models.CharField(default='Email / Chat', max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='BlazingHog', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    concept = models.CharField(max_length=100)
    email_chat_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    query_type = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=100)

    # questions
    # solutions
    solution_1 = models.IntegerField()
    solution_2 = models.IntegerField()
    solution_3 = models.IntegerField()
    solution_4 = models.IntegerField()

    # Efficiency
    efficiency_1 = models.IntegerField()
    efficiency_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    # Scores
    solution_score = models.IntegerField()
    efficiency_score = models.IntegerField()
    compliance_score = models.IntegerField()
    overall_score = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class NoomPod(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Noompod', max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Noompod', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    evaluator_name = models.CharField(max_length=100)
    transaction_handled_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    team_lead = models.CharField(max_length=100)
    ticket_number = models.CharField(max_length=50)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    # Customer Experience
    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()
    compliance_6 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    ce_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class NoomEva(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Noomeva', max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Noomeva', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    evaluator_name = models.CharField(max_length=100)
    transaction_handled_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    team_lead = models.CharField(max_length=100)
    ticket_number = models.CharField(max_length=50)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    # Customer Experience
    ce_1 = models.IntegerField()
    ce_2 = models.IntegerField()
    ce_3 = models.IntegerField()
    ce_4 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()
    compliance_6 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    ce_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class AbHindalco(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Abhindalco', max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Abhindalco', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)

    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    team_lead = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)

    # Opening and Closing
    oc_1 = models.IntegerField()
    oc_2 = models.IntegerField()
    oc_3 = models.IntegerField()
    # SoftSkills
    softskill_1 = models.IntegerField()
    softskill_2 = models.IntegerField()
    softskill_3 = models.IntegerField()
    softskill_4 = models.IntegerField()
    # Business and Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    oc_total = models.IntegerField(null=True)
    softskill_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class Practo(models.Model):
    # Start Common Must Add to all models
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Practo', max_length=50)
    type = models.CharField(default='Email / Chat', max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Practo', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)
    # End Common Must Add to all models

    associate_name = models.CharField(max_length=150)
    emp_id = models.CharField(max_length=30)
    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=60)

    case_no = models.CharField(max_length=200, null=True, blank=True)
    issue_type = models.CharField(max_length=200, null=True, blank=True)
    sub_issue = models.CharField(max_length=200, null=True, blank=True)
    sub_sub_issue = models.CharField(max_length=200, null=True, blank=True)
    chat_date = models.DateField(null=True, blank=True)
    csat = models.CharField(max_length=200, null=True, blank=True)
    product = models.CharField(max_length=200, null=True, blank=True)

    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    team_lead = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)

    # Customer Experience
    p_1 = models.IntegerField()
    p1_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p1_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p1_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p1_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p1_s5 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p1_s6 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_2 = models.IntegerField()
    p_3 = models.IntegerField()
    p3_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p3_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p3_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p3_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p3_s5 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p3_s6 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_4 = models.IntegerField()
    p4_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p4_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p4_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p4_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p4_s5 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_5 = models.IntegerField()
    p_6 = models.IntegerField()
    p_7 = models.IntegerField()
    p7_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p7_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p7_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p7_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_8 = models.IntegerField()
    p8_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p8_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p8_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p8_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p8_s5 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p8_s6 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p8_s7 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_9 = models.IntegerField()
    p9_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p9_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p9_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p9_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p9_s5 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p9_s6 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_10 = models.IntegerField()
    p_11 = models.IntegerField()
    p11_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p11_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p11_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p11_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p11_s5 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p11_s6 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p11_s7 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_12 = models.IntegerField()
    p_13 = models.IntegerField()
    p_14 = models.IntegerField()
    p_15 = models.IntegerField()
    p15_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p15_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p15_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_16 = models.IntegerField()
    p_17 = models.IntegerField()
    p17_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p17_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p17_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p17_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p_18 = models.IntegerField(null=True, blank=True)
    p18_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p18_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p18_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    p18_s4 = models.CharField(max_length=20, default="Yes", null=True, blank=True)

    compliance_1 = models.CharField(max_length=30)
    compliance1_s1 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    compliance1_s2 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    compliance1_s3 = models.CharField(max_length=20, default="Yes", null=True, blank=True)
    compliance_2 = models.CharField(max_length=30)

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class FameHouse(models.Model):
    # Start Common Must Add to all models
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Fame House', max_length=50)
    type = models.CharField(default='Email / Chat', max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Fame', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)
    # End Common Must Add to all models

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)

    ticket_no = models.CharField(max_length=50)
    ticket_type = models.CharField(max_length=50)
    trans_date = models.DateField()

    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    team_lead = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)

    # Immediate fails:
    compliance_1 = models.IntegerField(null=True)
    compliance_2 = models.IntegerField(null=True)
    compliance_3 = models.IntegerField(null=True)
    compliance_4 = models.IntegerField(null=True)
    compliance_5 = models.IntegerField(null=True)
    compliance_6 = models.IntegerField(null=True)
    compliance_7 = models.IntegerField(null=True)
    compliance_8 = models.IntegerField(null=True)
    compliance_9 = models.IntegerField(null=True)
    compliance_10 = models.IntegerField(null=True)
    compliance_11 = models.IntegerField(null=True)

    # customer Response
    cr_1 = models.CharField(max_length=10, null=True)
    # Opening
    opening_1 = models.CharField(max_length=10, null=True)
    opening_2 = models.CharField(max_length=10, null=True)
    # Composition
    comp_1 = models.CharField(max_length=10, null=True)
    comp_2 = models.CharField(max_length=10, null=True)
    # Macro Usage
    macro_1 = models.CharField(max_length=10, null=True)
    macro_2 = models.CharField(max_length=10, null=True)
    # Closing
    closing_1 = models.CharField(max_length=10, null=True)
    closing_2 = models.CharField(max_length=10, null=True)
    # Customer Issue Resolution
    cir_1 = models.CharField(max_length=10, null=True)
    cir_2 = models.CharField(max_length=10, null=True)
    cir_3 = models.CharField(max_length=10, null=True)
    cir_4 = models.CharField(max_length=10, null=True)
    cir_5 = models.CharField(max_length=10, null=True)
    cir_6 = models.CharField(max_length=10, null=True)
    cir_7 = models.CharField(max_length=10, null=True)
    # Etiquette
    et_1 = models.CharField(max_length=10, null=True)
    et_2 = models.CharField(max_length=10, null=True)
    et_3 = models.CharField(max_length=10, null=True)
    et_4 = models.CharField(max_length=10, null=True)
    et_5 = models.CharField(max_length=10, null=True)
    # Documentation
    doc_1 = models.CharField(max_length=10, null=True)
    doc_2 = models.CharField(max_length=10, null=True)
    doc_3 = models.CharField(max_length=10, null=True)
    doc_4 = models.CharField(max_length=10, null=True)

    compliance_total = models.IntegerField(null=True)

    overall_score = models.IntegerField(null=True)

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class ILMakiage(models.Model):
    # Start Common Must Add to all models
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='IL Makiage', max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='ILM', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)
    # End Common Must Add to all models

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=15)
    email_chat_date = models.DateField()
    query_type = models.CharField(max_length=100)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)

    # solution
    s_1 = models.IntegerField()
    s_2 = models.IntegerField()
    s_3 = models.IntegerField()
    s_4 = models.IntegerField()

    # Efficiency
    e_1 = models.IntegerField()
    e_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class Winopoly(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Winopoly Outbound', max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Winopoly', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=150)
    quality_analyst = models.CharField(max_length=150)
    customer_name = models.CharField(max_length=150)
    customer_contact = models.CharField(max_length=100)
    audit_date = models.DateField()
    zone = models.CharField(max_length=150)
    concept = models.CharField(max_length=160)
    call_date = models.DateField()
    call_duration = models.IntegerField()
    disposition = models.CharField(max_length=150)
    team_lead = models.CharField(max_length=150)
    team_lead_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=150)
    manager_id = models.IntegerField()
    am = models.CharField(max_length=150)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # Opening Statement
    comp_1 = models.IntegerField()
    op_2 = models.IntegerField()
    op_3 = models.IntegerField()
    op_4 = models.IntegerField()
    op_5 = models.IntegerField()

    # MATCHING PROCESS
    mp_1 = models.IntegerField()
    mp_2 = models.IntegerField()
    mp_3 = models.IntegerField()

    # CALL HANDLING PROCESS
    cp_1 = models.IntegerField()
    cp_2 = models.IntegerField()
    cp_3 = models.IntegerField()
    cp_4 = models.IntegerField()
    cp_5 = models.IntegerField()
    cp_6 = models.IntegerField()

    #  Compliance
    comp_2 = models.IntegerField()
    comp_3 = models.IntegerField()
    comp_4 = models.IntegerField()
    comp_5 = models.IntegerField()

    # TP
    tp_1 = models.IntegerField()
    tp_2 = models.IntegerField()
    tp_3 = models.IntegerField()
    comp_6 = models.IntegerField()

    evaluator_comment = models.TextField()
    coaching_comment = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True, blank=True)
    emp_comments = models.TextField(null=True, blank=True)
    # Total Scores
    overall_score = models.IntegerField(null=True, blank=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class Nerotel(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Nerotel Inbound', max_length=50)
    type = models.CharField(default='Inbound', max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Nerotel', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)

    zone = models.CharField(max_length=50)
    concept = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=15)
    call_date = models.DateField()
    call_duration = models.IntegerField(null=True, blank=True)
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    am = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager_id = models.CharField(max_length=30)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # Engagement
    eng_1 = models.IntegerField()
    eng_2 = models.IntegerField()
    eng_3 = models.IntegerField()
    eng_4 = models.IntegerField()
    eng_5 = models.IntegerField()
    eng_6 = models.IntegerField()
    eng_7 = models.IntegerField()
    eng_8 = models.IntegerField()
    eng_9 = models.IntegerField()
    # Resolution
    res_1 = models.IntegerField()
    res_2 = models.IntegerField()
    res_3 = models.IntegerField()
    res_4 = models.IntegerField()
    # Business needs
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    # Scores
    eng_total = models.IntegerField(null=True)
    res_total = models.IntegerField(null=True)
    compliance_total = models.IntegerField(null=True)
    overall_score = models.IntegerField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class SpoiledChild(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Spoiled Child', max_length=50)
    type = models.CharField(default='Email / Chat', max_length=50, null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Spoiled', max_length=50)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    concept = models.CharField(max_length=100)
    email_chat_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)
    query_type = models.CharField(max_length=100)
    ticket_id = models.CharField(max_length=100)

    # questions
    # solutions
    solution_1 = models.IntegerField()
    solution_2 = models.IntegerField()
    solution_3 = models.IntegerField()
    solution_4 = models.IntegerField()

    # Efficiency
    efficiency_1 = models.IntegerField()
    efficiency_2 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    # Scores
    solution_score = models.IntegerField()
    efficiency_score = models.IntegerField()
    compliance_score = models.IntegerField()
    overall_score = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)


class Amerisave(models.Model):
    unique_id = models.CharField(max_length=300)
    campaign = models.CharField(max_length=150)
    campaign_id = models.IntegerField(null=True, blank=True)
    campaign_type = models.CharField(default='Amerisave', max_length=50)
    category = models.CharField(max_length=150, null=True, blank=True)
    page_type = models.CharField(default='Amerisave', max_length=50)
    type = models.CharField(max_length=150, null=True, blank=True)
    audit_id = models.CharField(max_length=100, null=True, blank=True)

    emp_id = models.CharField(max_length=30)
    associate_name = models.CharField(max_length=50)
    transfer = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=100)
    lead_source = models.CharField(max_length=100)
    call_date = models.DateField()
    audit_date = models.DateField()
    quality_analyst = models.CharField(max_length=100)
    team_lead = models.CharField(max_length=100)
    team_lead_id = models.CharField(max_length=30)
    manager = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=30)
    am = models.CharField(max_length=100)
    am_id = models.CharField(max_length=30)
    week = models.CharField(max_length=10)

    # questions
    # NCE
    nce_1 = models.IntegerField()
    nce_2 = models.CharField(max_length=100)
    nce_3 = models.IntegerField()
    nce_4 = models.IntegerField()

    # Compliance
    compliance_1 = models.IntegerField()
    compliance_2 = models.IntegerField()
    compliance_3 = models.IntegerField()
    compliance_4 = models.IntegerField()
    compliance_5 = models.IntegerField()
    compliance_6 = models.IntegerField()

    # Scores
    nce_score = models.IntegerField()
    compliance_score = models.IntegerField()
    overall_score = models.IntegerField()

    areas_improvement = models.TextField()
    positives = models.TextField()
    comments = models.TextField()
    fail_type = models.CharField(max_length=80)

    added_by = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    closed_date = models.DateTimeField(null=True)
    emp_comments = models.TextField(null=True)

    fatal = models.BooleanField(default=False)
    fatal_count = models.IntegerField(default=0)
    dispute_status = models.BooleanField(default=False)
    audit_duration = models.CharField(max_length=30)
