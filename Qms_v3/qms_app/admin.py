from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here

class ProfileSearch(admin.ModelAdmin):
    search_fields = ('emp_name', 'emp_id')
    list_display = ('emp_name', 'emp_id', 'emp_desi', 'emp_process', "emp_rm1", "emp_rm2", "emp_rm3")

class CampaignResourse(resources.ModelResource):
    class Meta:
        model = Campaign

class CampaignSearch(ImportExportModelAdmin):
    search_fields = ('name', 'type')
    list_display = ('name', 'type', 'page_type', 'category', 'threshold')
    resource_class = CampaignResourse

class CampaignMappingSearch(admin.ModelAdmin):
    search_fields = ('qa', 'qa_id', 'campaign')
    list_display = ('qa', 'qa_id', 'campaign')

class Search(admin.ModelAdmin):
    search_fields = ('campaign', 'associate_name', 'emp_id')
    list_display = ('associate_name', 'campaign', 'emp_id', 'quality_analyst', 'overall_score')


class EmployeesProfileResourse(resources.ModelResource):
    class Meta:
        model = EmployeesProfile

class EmployeesProfileSearch(ImportExportModelAdmin):
    search_fields = ('emp_name', 'emp_id')
    list_display = ('emp_name', 'emp_id', 'emp_desi', 'emp_process', "emp_rm1", "emp_rm2", "emp_rm3")
    list_filter = ['agent_status']
    resource_class = EmployeesProfileResourse

admin.site.register(Campaign, CampaignSearch)
admin.site.register(CampaignMapping, CampaignMappingSearch)
admin.site.register(Profile, ProfileSearch)
admin.site.register(EmployeesProfile, EmployeesProfileSearch)
admin.site.register(Outbound, Search)
admin.site.register(Inbound, Search)
admin.site.register(EmailChat, Search)
admin.site.register(DigitalSwissGold, Search)
admin.site.register(FLA, Search)
admin.site.register(BlazingHog, Search)
admin.site.register(NoomPod, Search)
admin.site.register(NoomEva, Search)
admin.site.register(Practo, Search)
admin.site.register(FameHouse, Search)
admin.site.register(ILMakiage, Search)
admin.site.register(Winopoly, Search)
admin.site.register(Nerotel, Search)
admin.site.register(SpoiledChild, Search)
admin.site.register(Amerisave, Search)
admin.site.register(AbHindalco, Search)
admin.site.register(AuditIdTable)
