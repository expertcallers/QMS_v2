from rest_framework import serializers

from .models import *


class OutboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbound
        fields = ['campaign', 'associate_name', 'emp_id', "zone", "concept", "customer_name", "customer_contact",
                  "call_date",
                  'call_duration', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id', 'am', 'am_id', 'week', 'oc_1', 'oc_2', 'oc_3', 'softskill_1', 'softskill_2',
                  'softskill_3',
                  'softskill_4', 'softskill_5', 'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4',
                  'compliance_5',
                  'compliance_6', 'areas_improvement', 'positives', 'comments', 'status', 'closed_date', 'emp_comments',
                  'oc_total', 'softskill_total', 'compliance_total', 'overall_score', 'fatal', 'fatal_count',
                  'dispute_status',
                  'audit_duration']


class InboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbound
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'customer_contact',
                  'call_date',
                  'call_duration', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 'ce_1', 'ce_2', 'ce_3', 'ce_4', 'ce_5', 'ce_6', 'ce_7', 'ce_8', 'ce_9',
                  'ce_10', 'ce_11',
                  'business_1', 'business_2', 'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4',
                  'compliance_5',
                  'areas_improvement', 'positives', 'comments', 'status', 'closed_date', 'emp_comments', 'ce_total',
                  'business_total',
                  'compliance_total', 'overall_score', 'fatal', 'fatal_count', 'dispute_status', 'audit_duration']


class EmailChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailChat
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'customer_contact',
                  'call_date',
                  'call_duration', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 'ce_1', 'ce_2', 'ce_3', 'ce_4', 'ce_5', 'ce_6', 'ce_7', 'ce_8', 'ce_9',
                  'ce_10', 'ce_11',
                  'business_1', 'business_2', 'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4',
                  'compliance_5',
                  'areas_improvement', 'positives', 'comments', 'status', 'closed_date', 'emp_comments', 'ce_total',
                  'business_total',
                  'compliance_total', 'overall_score', 'fatal', 'fatal_count', 'dispute_status', 'audit_duration']


class DigitalSwissGoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalSwissGold
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'customer_contact',
                  'call_date',
                  'call_duration', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 'ce_1', 'ce_2', 'ce_3', 'ce_4', 'ce_5', 'ce_6', 'ce_7', 'ce_8', 'ce_9',
                  'ce_10', 'ce_11',
                  'business_1', 'business_2', 'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4',
                  'compliance_5',
                  'areas_improvement', 'positives', 'comments', 'status', 'closed_date', 'emp_comments', 'ce_total',
                  'business_total',
                  'compliance_total', 'overall_score', 'fatal', 'fatal_count', 'dispute_status', 'audit_duration']


class FLASerializer(serializers.ModelSerializer):
    class Meta:
        model = FLA
        fields = ['campaign', 'associate_name', 'emp_id', 'concept', 'transaction_handles_date', 'service', 'order_id',
                  'check_list', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 'reason_for_failure', 'areas_improvement', 'positives', 'comments', 'status',
                  'closed_date',
                  'emp_comments', 'overall_score', 'fatal', 'fatal_count', 'dispute_status', 'audit_duration']


class BlazingHogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlazingHog
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'email_chat_date',
                  'query_type',
                  'ticket_id', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 'solution_1', 'solution_2', 'solution_3', 'solution_4', 'efficiency_1',
                  'efficiency_2',
                  'compliance_1', 'compliance_2', 'compliance_3', 'areas_improvement', 'positives', 'comments',
                  'status',
                  'closed_date', 'emp_comments', 'solution_score', 'efficiency_score', 'compliance_score',
                  'overall_score', 'fatal',
                  'fatal_count', 'dispute_status', 'audit_duration']


class NoomPodSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoomPod
        fields = ['campaign', 'associate_name', 'emp_id', 'concept', 'evaluator_name', 'transaction_handled_date',
                  'ticket_number',
                  'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager', 'manager_id',
                  'am', 'am_id', 'week', 'ce_1', 'ce_2', 'ce_3', 'ce_4', 'compliance_1', 'compliance_2', 'compliance_3',
                  'compliance_4', 'compliance_5', 'compliance_6', 'areas_improvement', 'positives', 'comments',
                  'status',
                  'closed_date', 'emp_comments', 'ce_total', 'compliance_total', 'overall_score', 'fatal',
                  'fatal_count', 'dispute_status', 'audit_duration']


class NoomEvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoomEva
        fields = ['campaign', 'associate_name', 'emp_id', 'concept', 'evaluator_name', 'transaction_handled_date',
                  'ticket_number',
                  'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager', 'manager_id',
                  'am', 'am_id', 'week', 'ce_1', 'ce_2', 'ce_3', 'ce_4', 'compliance_1', 'compliance_2', 'compliance_3',
                  'compliance_4', 'compliance_5', 'compliance_6', 'areas_improvement', 'positives', 'comments',
                  'status',
                  'closed_date', 'emp_comments', 'ce_total', 'compliance_total', 'overall_score', 'fatal',
                  'fatal_count', 'dispute_status', 'audit_duration']


class AbHindalcoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbHindalco
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'customer_contact',
                  'call_date',
                  'call_duration', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 'oc_1', 'oc_2', 'oc_3', 'softskill_1', 'softskill_2', 'softskill_3',
                  'softskill_4', 'compliance_1',
                  'compliance_2', 'compliance_3', 'compliance_4', 'areas_improvement', 'positives', 'comments',
                  'status', 'closed_date',
                  'emp_comments', 'oc_total', 'softskill_total', 'compliance_total', 'overall_score', 'fatal',
                  'fatal_count',
                  'dispute_status', 'audit_duration']


class FameHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FameHouse
        fields = ['campaign', 'associate_name', 'emp_id', 'ticket_no', 'ticket_type', 'trans_date',
                  'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager', 'manager_id',
                  'am', 'am_id', 'week', 'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5',
                  'compliance_6', 'compliance_7', 'compliance_8', 'compliance_9', 'compliance_10', 'compliance_11',
                  'cr_1', 'opening_1', 'opening_2', 'comp_1', 'comp_2', 'macro_1', 'macro_2', 'closing_1', 'closing_2',
                  'cir_1', 'cir_2', 'cir_3', 'cir_4', 'cir_5', 'cir_6', 'cir_7', 'et_1', 'et_2', 'et_3', 'et_4', 'et_5',
                  'doc_1', 'doc_2', 'doc_3', 'doc_4', 'areas_improvement', 'positives', 'comments', 'status',
                  'closed_date', 'emp_comments', 'compliance_total', 'overall_score', 'fatal',
                  'fatal_count', 'dispute_status', 'audit_duration']


class PractoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practo
        fields = ['campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'case_no', 'issue_type', 'sub_issue',
                  'sub_sub_issue', 'chat_date', 'csat', 'product',
                  'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager', 'manager_id',
                  'am', 'am_id', 'week',
                  'p_1', 'p1_s1', 'p1_s2', 'p1_s3', 'p1_s4', 'p1_s5', 'p1_s6', 'p_2', 'p_3', 'p3_s1', 'p3_s2', 'p3_s3',
                  'p3_s4', 'p3_s5', 'p3_s6', 'p_4', 'p4_s1', 'p4_s2', 'p4_s3', 'p4_s4', 'p4_s5', 'p_5', 'p_6', 'p_7',
                  'p7_s1', 'p7_s2', 'p7_s3', 'p7_s4', 'p_8', 'p8_s1', 'p8_s2', 'p8_s3', 'p8_s4', 'p8_s5', 'p8_s6',
                  'p8_s7', 'p_9', 'p9_s1', 'p9_s2', 'p9_s3', 'p9_s4', 'p9_s5', 'p9_s6', 'p_10', 'p_11', 'p11_s1',
                  'p11_s2', 'p11_s3', 'p11_s4', 'p11_s5', 'p11_s6', 'p11_s7', 'p_12', 'p_13', 'p_14', 'p_15', 'p15_s1',
                  'p15_s2', 'p15_s3', 'p_16', 'p_17', 'p17_s1', 'p17_s2', 'p17_s3', 'p17_s4', 'p_18', 'p18_s1',
                  'p18_s2', 'p18_s3', 'p18_s4', 'compliance_1', 'compliance1_s1', 'compliance1_s2', 'compliance1_s3',
                  'compliance_2',
                  'areas_improvement', 'positives', 'comments',
                  'status',
                  'closed_date', 'emp_comments', 'overall_score', 'fatal',
                  'fatal_count', 'dispute_status', 'audit_duration']


class ILMakiageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ILMakiage
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'ticket_id',
                  'email_chat_date',
                  'query_type', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 's_1', 's_2', 's_3', 's_4', 'e_1', 'e_2', 'compliance_1', 'compliance_2',
                  'compliance_3',
                  'areas_improvement', 'positives', 'comments', 'status', 'closed_date',
                  'emp_comments', 'overall_score', 'fatal', 'fatal_count',
                  'dispute_status', 'audit_duration']


class WinopolySerializer(serializers.ModelSerializer):
    class Meta:
        model = Winopoly
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'customer_contact',
                  'call_date',
                  'call_duration', 'audit_date', 'disposition', 'quality_analyst', 'added_by', 'team_lead',
                  'team_lead_id', 'manager', 'manager_id',
                  'am', 'am_id', 'week', 'comp_1', 'op_2', 'op_3', 'op_4', 'op_5', 'mp_1', 'mp_2', 'mp_3', 'cp_1',
                  'cp_2', 'cp_3', 'cp_4', 'cp_5', 'cp_6',
                  'comp_2', 'comp_3', 'comp_4', 'comp_5', 'tp_1', 'tp_2', 'tp_3', 'comp_6', 'evaluator_comment',
                  'coaching_comment',
                  'status', 'closed_date', 'emp_comments', 'overall_score', 'fatal', 'fatal_count', 'dispute_status',
                  'audit_duration']


class NerotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nerotel
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'customer_contact',
                  'call_date',
                  'call_duration', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 'eng_1', 'eng_2', 'eng_3', 'eng_4', 'eng_5', 'eng_6', 'eng_7', 'eng_8',
                  'eng_9', 'res_1', 'res_2',
                  'res_3', 'res_4', 'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'areas_improvement',
                  'positives',
                  'comments', 'eng_total', 'res_total', 'compliance_total', 'overall_score',
                  'status', 'closed_date', 'emp_comments', 'fatal', 'fatal_count', 'dispute_status', 'audit_duration']


class SpoiledChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpoiledChild
        fields = ['campaign', 'associate_name', 'emp_id', "zone", 'concept', 'customer_name', 'email_chat_date',
                  'query_type',
                  'ticket_id', 'audit_date', 'quality_analyst', 'added_by', 'team_lead', 'team_lead_id', 'manager',
                  'manager_id',
                  'am', 'am_id', 'week', 'solution_1', 'solution_2', 'solution_3', 'solution_4', 'efficiency_1',
                  'efficiency_2',
                  'compliance_1', 'compliance_2', 'compliance_3', 'areas_improvement', 'positives',
                  'comments', 'solution_score', 'efficiency_score', 'compliance_score', 'overall_score',
                  'status', 'closed_date', 'emp_comments', 'fatal', 'fatal_count', 'dispute_status', 'audit_duration']
