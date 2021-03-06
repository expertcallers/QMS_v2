from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('login', Login),
    path('logout', logoutUser),
    path('change-password', change_password_new),
    path('dashboard', DashboardRedirect),
    path('qa-dashboard', qaDashboard),
    path('manager-dashboard', managerDashboard),
    path('qa-manager-dashboard', QAmanagerDashboard),
    path('get-emp', getEmp),
    path('form', formView),
    path('qa-reports/<str:type>', ReportTable),
    path('manager-reports/<str:type>', ManagerReportTable),
    path('qa-month-reports/<str:type>', MonthReportTable),
    path('report', qaReport),
    path('report/<int:id>/<str:type>', EmailReport),
    path('agent-dashboard', agentDashbaoard),
    path('emp-report/<str:type>', agentReportTable),
    path('agent-report/<str:type>/<str:emp_id>', IndividualAgentReportTable),
    path('individual-report', IndividualReportView),
    path('campaign-agent-report', CampaignAgentReportView),
    path('agent-report', agentReport),
    path('agent-respond', agentRespond),

    path('export', exportData),

    # Form Submits
    path('outbound-submit', outboundFormSubmit),
    path('inbound-submit', inboundFormSubmit),
    path('email-submit', emailFormSubmit),
    path('digital-submit', DigitalSwissGoldFormSubmit),
    path('fla-submit', FLAFormSubmit),
    path('blazinghog-submit', blazingHogFormSubmit),
    path('noompod-submit', NoomPodFormSubmit),
    path('noomeva-submit', NoomEvaFormSubmit),
    path('abhindalco-submit', AbHindalcoFormSubmit),
    path('practo-submit', PractoSubmit),
    path('fame-submit', fameHouseSubmit),
    path('ilm-submit', ILMakiageSubmit),
    path('winopoly-submit', WinopolySubmit),
    path('nerotel-submit', NerotelSubmit),
    path('spoiled-submit', SpoiledChildSubmit),
    path('amerisave-submit', AmerisaveSubmit),

    path('password-reset', PasswordReset),
    path('add-email', AddEmail),
    path('verify-email', VerifyEmail),
    path('edit-email', EditEmail),
    path('add-user', AddUser),
    path('add-campaign', AddCampaign),
    path('add-qa-mapping', AddQaMapping),
    path('view-qa-mapping', viewQaMapping),
    path('edit-email', EditEmail),
    path("settings", change_password),
    path("delete-qa-mapping", deleteQaMapping),
    path("total-list", TotalList.as_view(), name="to_show_the_total_list_of_tables"),
    path('create-users', createUser),


]
