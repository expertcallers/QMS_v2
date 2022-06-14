import datetime
from datetime import date

import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from drf_multiple_model.views import FlatMultipleModelAPIView

from .serializers import *

# Create your views here.

# Campaign Models
campaign_list = [Outbound, Inbound, EmailChat,
                 DigitalSwissGold, FLA, BlazingHog, NoomPod, NoomEva, AbHindalco,
                 Practo, FameHouse, ILMakiage, Winopoly, Nerotel, SpoiledChild, Amerisave]

# page names must be equal to campaign page type
pages = ["Outbound", "Inbound", "Email", "Digital", "FLA", "BlazingHog", "Noompod", "Noomeva", "Abhindalco", "Practo",
         "Fame", "ILM", "Winopoly", "Nerotel", "Spoiled", 'Amerisave']

# List of Agents Designations
agent_list = ["CRO", "Patrolling officer"]

# List of Managers Designations
mgr_list = ["Manager"]

# List of QA Designations
qa_list = ["QA"]

# Calculating first and today's date
currentMonth = datetime.datetime.now().month
currentYear = datetime.datetime.now().year
month_start_date = datetime.datetime(currentYear, currentMonth, 1)
todays_date = date.today()


def index(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "index.html")


def logoutUser(request):
    logout(request)
    return redirect('/')


def Login(request):
    if request.method == "POST":
        username = request.POST["user"]
        password = request.POST["pass"]
        user = authenticate(username=username, password=password)
        if user is not None:
            # user_login
            login(request, user)
            pc = request.user.profile.pc
            if pc == False:
                return redirect("/change-password")
            else:
                return redirect("/dashboard")
        else:
            messages.info(request, 'Invalid user !')
            return redirect("/logout")
    else:
        pass


@login_required
def change_password(request):  # Test1
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            user = request.user
            user.profile.pc = True
            user.save()
            user.profile.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/logout')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'settings.html', {'form': form})


@login_required
def DashboardRedirect(request):
    designation = request.user.profile.emp_desi
    if designation in qa_list:
        return redirect("/qa-dashboard")
    elif designation in mgr_list:
        return redirect("/manager-dashboard")
    elif designation in agent_list:
        return redirect("/agent-dashboard")
    else:
        messages.info(request, 'Invalid Request. You have been logged out :)')
        return redirect("/logout")


# QA Dashboard (qa-dashboard)
@login_required
def managerDashboard(request):
    user = request.user
    if user.profile.emp_desi in mgr_list:
        campaigns = Campaign.objects.all()
        profile = Profile.objects.filter(emp_desi__in=agent_list)
        qa_profile = Profile.objects.filter(emp_desi__in=qa_list)
        tl_profile = Profile.objects.filter(emp_desi="Team Leader")
        am_profile = Profile.objects.filter(emp_desi="Assistant Manager")
        # All Audits
        all_total_count = []
        for i in campaign_list:
            campaign = i.objects.all().count()
            all_total_count.append(campaign)
        all_total = 0
        for i in all_total_count:
            all_total += i

        # All Audits Current Month

        # All Audits Current Month Count
        month_all_count = []
        for i in campaign_list:
            camapign = i.objects.filter(audit_date__range=[month_start_date, todays_date]).count()
            month_all_count.append(camapign)
        month_all_total = 0
        for i in month_all_count:
            month_all_total += i

        # Month's Average Score
        camapign_score = 0
        for i in campaign_list:
            score = i.objects.filter(audit_date__range=[month_start_date, todays_date])
            for j in score:
                camapign_score += j.overall_score
        if month_all_total == 0:
            score_average = "No Audits This Month"
        else:
            score_average = (camapign_score) / month_all_total

        # Month's Fatal Count
        fatal_count = 0
        for i in campaign_list:
            fatal = i.objects.filter(audit_date__range=[month_start_date, todays_date])
            for j in fatal:
                fatal_count += j.fatal_count

        # Open Audits
        open_count = []
        for i in campaign_list:
            campaign = i.objects.filter(status=False).count()
            open_count.append(campaign)
        open_total = 0
        for i in open_count:
            open_total += i

        # Dispute Audits
        dispute_count = []
        for i in campaign_list:
            campaign = i.objects.filter(dispute_status=True).count()
            dispute_count.append(campaign)
        dispute_total = 0
        for i in dispute_count:
            dispute_total += i

        # Fatal Audits
        fatal_audit_count = []
        for i in campaign_list:
            campaign = i.objects.filter(fatal=True,
                                        audit_date__range=[month_start_date, todays_date]).count()
            fatal_audit_count.append(campaign)
        fatal_total = 0
        for i in fatal_audit_count:
            fatal_total += i

        # Coaching Closure
        closure_count_list = []
        for i in campaign_list:
            campaign = i.objects.filter(status=True).count()
            closure_count_list.append(campaign)
        closure_count = 0
        for i in closure_count_list:
            closure_count += i

        if all_total == 0:
            coaching_closure = "No Audits"
        else:
            coaching_closure = (closure_count / all_total) * 100

        tot = []
        for i in campaign_list:
            campaign = i.objects.filter(status=False)
            tot.append(campaign)

        audits = []
        for j in profile:
            average_score = 0
            d = {}
            report_all_total = 0
            report_all_total_count = []
            for i in campaign_list:
                campaign = i.objects.filter(emp_id=j.emp_id)
                if campaign.count() > 0:
                    score_list = []
                    for k in campaign:
                        score_list.append(k.overall_score)
                    for number in score_list:
                        average_score += number
                        report_all_total += 1
            if report_all_total > 0:
                d["score"] = average_score / report_all_total
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            else:
                d["score"] = "No Audits"
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            for f in report_all_total_count:
                report_all_total += f
            audits.append(d)

        new_audits = []
        for i in audits:
            if i["score"] != "No Audits":
                new_audits.append(i)

        qa_audits = []
        for j in qa_profile:
            average_score = 0
            d = {}
            report_all_total = 0
            report_all_total_count = []
            for i in campaign_list:
                campaign = i.objects.filter(added_by=j.emp_id)
                if campaign.count() > 0:
                    score_list = []
                    for k in campaign:
                        score_list.append(k.overall_score)
                    for number in score_list:
                        average_score += number
                        report_all_total += 1
            if report_all_total > 0:
                d["score"] = average_score / report_all_total
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            else:
                d["score"] = "No Audits"
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            for f in report_all_total_count:
                report_all_total += f
            qa_audits.append(d)

        new_qa_audits = []
        for i in qa_audits:
            if i["score"] != "No Audits":
                new_qa_audits.append(i)

        tl_audits = []
        for j in tl_profile:
            average_score = 0
            d = {}
            report_all_total = 0
            report_all_total_count = []
            for i in campaign_list:
                campaign = i.objects.filter(team_lead_id=j.emp_id)
                if campaign.count() > 0:
                    score_list = []
                    for k in campaign:
                        score_list.append(k.overall_score)
                    for number in score_list:
                        average_score += number
                        report_all_total += 1
            if report_all_total > 0:
                d["score"] = average_score / report_all_total
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            else:
                d["score"] = "No Audits"
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            for f in report_all_total_count:
                report_all_total += f
            tl_audits.append(d)

        new_tl_audits = []
        for i in tl_audits:
            if i["score"] != "No Audits":
                new_tl_audits.append(i)

        am_audits = []
        for j in am_profile:
            average_score = 0
            d = {}
            report_all_total = 0
            report_all_total_count = []
            for i in campaign_list:
                campaign = i.objects.filter(am_id=j.emp_id)
                if campaign.count() > 0:
                    score_list = []
                    for k in campaign:
                        score_list.append(k.overall_score)
                    for number in score_list:
                        average_score += number
                        report_all_total += 1
            if report_all_total > 0:
                d["score"] = average_score / report_all_total
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            else:
                d["score"] = "No Audits"
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            for f in report_all_total_count:
                report_all_total += f
            am_audits.append(d)

        new_am_audits = []
        for i in am_audits:
            if i["score"] != "No Audits":
                new_am_audits.append(i)

        data = {"campaigns": campaigns, "profile": profile, "audit": tot,
                "month_all_total": month_all_total, "open_total": open_total, "dispute_total": dispute_total,
                "average": score_average, "fatal": fatal_count,
                "all_total": all_total, "fatal_total": fatal_total, "coaching_closure": coaching_closure,
                "audits": new_audits, "qa_audits": new_qa_audits, "tl_audits": new_tl_audits,
                "am_audits": new_am_audits}

        return render(request, "manager_dashboard.html", data)
    else:
        messages.info(request, 'Invalid Request. You have been logged out :)')
        return redirect("/logout")


# QA Dashboard (qa-dashboard)
@login_required
def qaDashboard(request):
    user = request.user
    emp_id = request.user.profile.emp_id
    if user.profile.emp_desi in qa_list:
        assigned_campaigns = CampaignMapping.objects.filter(qa_id=emp_id).values('campaign')
        campaigns = Campaign.objects.filter(id__in=assigned_campaigns)
        out_campaigns = CampaignMapping.objects.filter(qa_id=emp_id, campaign__type='Outbound')
        in_campaign = CampaignMapping.objects.filter(qa_id=emp_id, campaign__type='Inbound')
        email_campaign = CampaignMapping.objects.filter(qa_id=emp_id, campaign__type='Email / Chat')
        other_campaign = CampaignMapping.objects.filter(qa_id=emp_id).exclude(
            campaign__type__in=['Outbound', 'Inbound', 'Email / Chat'])
        profile = Profile.objects.filter(emp_desi__in=agent_list)

        # All Audits
        all_total_count = []
        for i in campaign_list:
            campaign = i.objects.filter(added_by=emp_id).count()
            all_total_count.append(campaign)
        all_total = 0
        for i in all_total_count:
            all_total += i

        # All Audits Current Month

        # All Audits Current Month Count
        month_all_count = []
        for i in campaign_list:
            camapign = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date]).count()
            month_all_count.append(camapign)
        month_all_total = 0
        for i in month_all_count:
            month_all_total += i

        # Month's Average Score
        camapign_score = 0
        for i in campaign_list:
            score = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date])
            for j in score:
                camapign_score += j.overall_score
        if month_all_total == 0:
            score_average = "No Audits This Month"
        else:
            score_average = (camapign_score) / month_all_total

        # Month's Fatal Count
        fatal_count = 0
        for i in campaign_list:
            fatal = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date])
            for j in fatal:
                fatal_count += j.fatal_count

        # Open Audits
        open_count = []
        for i in campaign_list:
            campaign = i.objects.filter(added_by=emp_id, status=False).count()
            open_count.append(campaign)
        open_total = 0
        for i in open_count:
            open_total += i

        # Dispute Audits
        dispute_count = []
        for i in campaign_list:
            campaign = i.objects.filter(added_by=emp_id, dispute_status=True).count()
            dispute_count.append(campaign)
        dispute_total = 0
        for i in dispute_count:
            dispute_total += i

        # Fatal Audits
        fatal_audit_count = []
        for i in campaign_list:
            campaign = i.objects.filter(added_by=emp_id, fatal=True,
                                        audit_date__range=[month_start_date, todays_date]).count()
            fatal_audit_count.append(campaign)
        fatal_total = 0
        for i in fatal_audit_count:
            fatal_total += i

        # Coaching Closure
        closure_count_list = []
        for i in campaign_list:
            campaign = i.objects.filter(added_by=emp_id, status=True).count()
            closure_count_list.append(campaign)
        closure_count = 0
        for i in closure_count_list:
            closure_count += i

        if all_total == 0:
            coaching_closure = "No Audits"
        else:
            coaching_closure = (closure_count / all_total) * 100

        tot = []
        for i in campaign_list:
            campaign = i.objects.filter(added_by=emp_id, status=False)
            tot.append(campaign)

        audits = []
        for j in profile:
            average_score = 0
            d = {}
            report_all_total = 0
            report_all_total_count = []
            for i in campaign_list:
                campaign = i.objects.filter(added_by=emp_id, emp_id=j.emp_id)
                campaign_count = i.objects.filter(added_by=emp_id, emp_id=j.emp_id).count()
                if campaign.count() > 0:
                    all_total_count.append(campaign_count)
                    score_list = []
                    for k in campaign:
                        score_list.append(k.overall_score)
                    for number in score_list:
                        average_score += number
                        report_all_total += 1
            if report_all_total > 0:
                d["score"] = average_score / report_all_total
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            else:
                d["score"] = "No Audits"
                d["associate_name"] = j.emp_name
                d["emp_id"] = j.emp_id
            for f in report_all_total_count:
                report_all_total += f
            audits.append(d)

        new_audits = []
        for i in audits:
            if i["score"] != "No Audits":
                new_audits.append(i)

        data = {"campaigns": campaigns, "out_campaigns": out_campaigns, "profile": profile, "in_campaign": in_campaign,
                "email_campaign": email_campaign, "other_campaign": other_campaign, "audit": tot,
                "month_all_total": month_all_total, "open_total": open_total, "dispute_total": dispute_total,
                "average": score_average, "fatal": fatal_count,
                "all_total": all_total, "fatal_total": fatal_total, "coaching_closure": coaching_closure,
                "audits": new_audits}

        return render(request, "qa_dashboard.html", data)
    else:
        messages.info(request, 'Invalid Request. You have been logged out :)')
        return redirect("/logout")


# Test function for ajax (get-emp)
def getEmp(request):
    if request.method == "POST":
        campaign = request.POST.get("campaign")
        profile = Profile.objects.filter(emp_process=campaign)
        return JsonResponse({"profile": profile}, status=200)


# QA Report Page (qa-reports/<str:type>)
@login_required
def ReportTable(request, type):
    emp_id = request.user.profile.emp_id

    def auditcalculator(type):
        audits = []
        if type == 'all':
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id)
                audits.append(tot_obj)
        elif type == "fatal":
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id, fatal=True,
                                           audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "month":
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "open":
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id, status=False)
                audits.append(tot_obj)
        elif type == "dispute":
            for i in campaign_list:
                tot_obj = i.objects.filter(added_by=emp_id, dispute_status=True)
                audits.append(tot_obj)
        elif type == "campaign-range":
            if request.method == "POST":
                cname = request.POST.get("campaign")
                status = request.POST.get("status")
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                for i in campaign_list:
                    if start_date:
                        if cname == "all" and status == "all":
                            tot_obj = i.objects.filter(added_by=emp_id, audit_date__range=[start_date, end_date])
                        elif cname == "all" and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, status=False,
                                                       audit_date__range=[start_date, end_date])
                        elif cname and status == "open":
                            cam = Campaign.objects.get(id=cname)
                            tot_obj = i.objects.filter(added_by=emp_id, campaign_id=cam.id, status=False,
                                                       audit_date__range=[start_date, end_date])
                        else:
                            cam = Campaign.objects.get(id=cname)
                            tot_obj = i.objects.filter(campaign_id=cam.id, added_by=emp_id,
                                                       audit_date__range=[start_date, end_date])
                        audits.append(tot_obj)
                    else:
                        if cname == "all" and status == "all":
                            tot_obj = i.objects.filter(added_by=emp_id)
                        elif cname == "all" and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, status=False)
                        elif cname and status == "open":
                            cam = Campaign.objects.get(id=cname)
                            tot_obj = i.objects.filter(added_by=emp_id, campaign_id=cam.id, status=False)
                        else:
                            cam = Campaign.objects.get(id=cname)
                            tot_obj = i.objects.filter(campaign_id=cam.id, added_by=emp_id)
                        audits.append(tot_obj)
            else:
                messages.info(request, "Invalid Request!")
                return redirect("/agent-dashboard")

        elif type == "emp-range":
            if request.method == "POST":
                emp = request.POST.get("emp_id")
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                status = request.POST.get("status")

                for i in campaign_list:
                    if start_date:
                        if emp == "all" and status == "all":
                            tot_obj = i.objects.filter(added_by=emp_id, audit_date__range=[start_date, end_date])
                        elif emp == "all" and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, status=False,
                                                       audit_date__range=[start_date, end_date])
                        elif emp and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, emp_id=emp, status=False,
                                                       audit_date__range=[start_date, end_date])
                        else:
                            tot_obj = i.objects.filter(emp_id=emp, added_by=emp_id,
                                                       audit_date__range=[start_date, end_date])
                        audits.append(tot_obj)
                    else:
                        if emp == "all" and status == "all":
                            tot_obj = i.objects.filter(added_by=emp_id)
                        elif emp == "all" and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, status=False)
                        elif emp and status == "open":
                            tot_obj = i.objects.filter(added_by=emp_id, emp_id=emp, status=False)
                        else:
                            tot_obj = i.objects.filter(emp_id=emp, added_by=emp_id)
                        audits.append(tot_obj)
            else:
                messages.info(request, "Invalid Request!")
                return redirect("/agent-dashboard")
        else:
            messages.info(request, 'Invalid Request. You have been logged out :)')
            return redirect("/logout")

        return audits

    audits = auditcalculator(type)
    data = {"audit": audits, "type": type, "qa_list": qa_list, "agent_list": agent_list, "mgr_list": mgr_list}
    return render(request, "qa_reports.html", data)


# Manager Report Page (qa-reports/<str:type>)
@login_required
def ManagerReportTable(request, type):
    def auditcalculator(type):
        audits = []
        if type == 'all':
            for i in campaign_list:
                tot_obj = i.objects.all()
                audits.append(tot_obj)
        elif type == "fatal":
            for i in campaign_list:
                tot_obj = i.objects.filter(fatal=True, audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "month":
            for i in campaign_list:
                tot_obj = i.objects.filter(audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "open":
            for i in campaign_list:
                tot_obj = i.objects.filter(status=False)
                audits.append(tot_obj)
        elif type == "dispute":
            for i in campaign_list:
                tot_obj = i.objects.filter(dispute_status=True)
                audits.append(tot_obj)
        elif type == "campaign-range":
            if request.method == "POST":
                cname = request.POST.get("campaign")
                status = request.POST.get("status")
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                for i in campaign_list:
                    if start_date:
                        if cname == "all" and status == "all":
                            tot_obj = i.objects.filter(audit_date__range=[start_date, end_date])
                        elif cname == "all" and status == "open":
                            tot_obj = i.objects.filter(status=False,
                                                       audit_date__range=[start_date, end_date])
                        elif cname and status == "open":
                            cam = Campaign.objects.get(id=cname)
                            tot_obj = i.objects.filter(campaign_id=cam.id, status=False,
                                                       audit_date__range=[start_date, end_date])
                        else:
                            cam = Campaign.objects.get(id=cname)
                            tot_obj = i.objects.filter(campaign_id=cam.id,
                                                       audit_date__range=[start_date, end_date])
                        if tot_obj not in audits:
                            audits.append(tot_obj)
                    else:
                        if cname == "all" and status == "all":
                            tot_obj = i.objects.all()
                        elif cname == "all" and status == "open":
                            tot_obj = i.objects.filter(status=False)
                        elif cname and status == "open":
                            cam = Campaign.objects.get(id=cname)
                            tot_obj = i.objects.filter(campaign_id=cam.id, status=False)
                        else:
                            cam = Campaign.objects.get(id=cname)
                            tot_obj = i.objects.filter(campaign_id=cam.id)
                        if tot_obj not in audits:
                            audits.append(tot_obj)
            else:
                messages.info(request, "Invalid Request!")
                return redirect("/agent-dashboard")

        elif type == "emp-range":
            if request.method == "POST":
                emp = request.POST.get("emp_id")
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                status = request.POST.get("status")

                for i in campaign_list:
                    if start_date:
                        if emp == "all" and status == "all":
                            tot_obj = i.objects.filter(audit_date__range=[start_date, end_date])
                        elif emp == "all" and status == "open":
                            tot_obj = i.objects.filter(status=False,
                                                       audit_date__range=[start_date, end_date])
                        elif emp and status == "open":
                            tot_obj = i.objects.filter(emp_id=emp, status=False,
                                                       audit_date__range=[start_date, end_date])
                        else:
                            tot_obj = i.objects.filter(emp_id=emp,
                                                       audit_date__range=[start_date, end_date])
                        audits.append(tot_obj)
                    else:
                        if emp == "all" and status == "all":
                            tot_obj = i.objects.all()
                        elif emp == "all" and status == "open":
                            tot_obj = i.objects.filter(status=False)
                        elif emp and status == "open":
                            tot_obj = i.objects.filter(emp_id=emp, status=False)
                        else:
                            tot_obj = i.objects.filter(emp_id=emp)
                        audits.append(tot_obj)
            else:
                messages.info(request, "Invalid Request!")
                return redirect("/agent-dashboard")
        else:
            messages.info(request, 'Invalid Request. You have been logged out :)')
            return redirect("/logout")

        return audits

    audits = auditcalculator(type)
    data = {"audit": audits, "type": type, "qa_list": qa_list, "agent_list": agent_list, "mgr_list": mgr_list}
    return render(request, "qa_reports.html", data)


# Form View (form)
@login_required
def formView(request):
    if request.method == "POST":
        campaign = request.POST["campaign"]

        emp = request.POST["emp"]
        campaign = Campaign.objects.get(id=campaign)
        type = campaign.page_type
        profile = Profile.objects.get(emp_id=emp)
        today = date.today()
        start = str(datetime.datetime.now().time())
        data = {"campaign": campaign, "profile": profile, "today": today, "start_time": start}

        for j in pages:
            if j == type:
                return render(request, "form/" + j + ".html", data)

    else:
        messages.info(request, 'Invalid Request !')
        return redirect("/logout")


# Report for QA (report)
@login_required
def qaReport(request):
    if request.method == "POST":
        id = request.POST["id"]
        type = request.POST["type"]

        for i in campaign_list:
            obj = i.objects.all()
            if obj.count() > 0:
                if obj[0].page_type == type:

                    audit = i.objects.get(id=id)
                    campaign = Campaign.objects.get(id=audit.campaign_id)

                    data = {"form": audit, 'campaign':campaign, 'mgr_list':mgr_list}
                    for j in pages:
                        if type == j:
                            return render(request, "report/" + j + ".html", data)
                else:
                    pass
            else:
                pass

    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


# Agent Dashbaoard (agent-dashboard)
@login_required
def agentDashbaoard(request):
    emp_id = request.user.profile.emp_id

    # All Audits
    all_total_count = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id).count()
        all_total_count.append(campaign)
    all_total = 0
    for i in all_total_count:
        all_total += i

    # All Audits Current Month

    # All Audits Current Month Count
    month_all_count = []
    for i in campaign_list:
        camapign = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date]).count()
        month_all_count.append(camapign)
    month_all_total = 0
    for i in month_all_count:
        month_all_total += i

    # Month's Average Score
    camapign_score = 0
    for i in campaign_list:
        score = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
        for j in score:
            camapign_score += j.overall_score
    if month_all_total == 0:
        score_average = "No Audits This Month"
    else:
        score_average = (camapign_score) / month_all_total

    # Month's Fatal Count
    fatal_count = 0
    for i in campaign_list:
        fatal = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
        for j in fatal:
            fatal_count += j.fatal_count

    # Open Audits
    open_count = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, status=False).count()
        open_count.append(campaign)
    open_total = 0
    for i in open_count:
        open_total += i

    # Dispute Audits
    dispute_count = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, dispute_status=True).count()
        dispute_count.append(campaign)
    dispute_total = 0
    for i in dispute_count:
        dispute_total += i

    # Fatal Audits
    fatal_audit_count = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, fatal=True,
                                    audit_date__range=[month_start_date, todays_date]).count()
        fatal_audit_count.append(campaign)
    fatal_total = 0
    for i in fatal_audit_count:
        fatal_total += i

    # Coaching Closure
    closure_count_list = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, status=True).count()
        closure_count_list.append(campaign)
    closure_count = 0
    for i in closure_count_list:
        closure_count += i

    if all_total == 0:
        coaching_closure = "No Audits"
    else:
        coaching_closure = (closure_count / all_total) * 100

    tot = []
    for i in campaign_list:
        campaign = i.objects.filter(emp_id=emp_id, status=False)
        tot.append(campaign)

    data = {
        "audit": tot, "month_all_total": month_all_total, "open_total": open_total, "dispute_total": dispute_total,
        "average": score_average, "fatal": fatal_count,
        "all_total": all_total, "fatal_total": fatal_total, "coaching_closure": coaching_closure
    }
    return render(request, "agent_dashboard.html", data)


# Agent Report Table (emp-report/<str:type>)
@login_required
def agentReportTable(request, type):
    emp_id = request.user.profile.emp_id

    def auditcalculator(type):
        audits = []
        if type == 'all':
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id)
                audits.append(tot_obj)
        elif type == "fatal":
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id, fatal=True, audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "month":
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
                audits.append(tot_obj)
        elif type == "open":
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id, status=False)
                audits.append(tot_obj)
        elif type == "dispute":
            for i in campaign_list:
                tot_obj = i.objects.filter(emp_id=emp_id, dispute_status=True)
                audits.append(tot_obj)
        elif type == "range":
            if request.method == "POST":
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                for i in campaign_list:
                    tot_obj = i.objects.filter(emp_id=emp_id, audit_date__range=[start_date, end_date])
                    audits.append(tot_obj)
            else:
                messages.info(request, "Invalid Request!")
                return redirect("/agent-dashboard")
        else:
            messages.info(request, 'Invalid Request.')
            return redirect("/logout")
        return audits

    audits = auditcalculator(type)
    data = {"audit": audits, "type": type, "qa_list": qa_list, "agent_list": agent_list, "mgr_list": mgr_list}
    return render(request, "agent_reports.html", data)


# Individual Agent Report Table (agent-report/<str:type>)
@login_required
def IndividualAgentReportTable(request, type, emp_id):
    designation = request.user.profile.emp_desi
    logged_emp_id = request.user.profile.emp_id
    if designation not in agent_list:
        def auditcalculator(type):
            audits = []
            emp_desi = Profile.objects.get(emp_id=emp_id).emp_desi
            if designation in mgr_list:
                if emp_desi in agent_list:
                    if type == 'all':
                        for i in campaign_list:
                            tot_obj = i.objects.filter(emp_id=emp_id)
                            audits.append(tot_obj)
                    elif type == "fatal":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(emp_id=emp_id, fatal=True,
                                                       audit_date__range=[month_start_date, todays_date])
                            audits.append(tot_obj)
                    elif type == "month":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
                            audits.append(tot_obj)
                    elif type == "open":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(emp_id=emp_id, status=False)
                            audits.append(tot_obj)
                    elif type == "dispute":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(emp_id=emp_id, dispute_status=True)
                            audits.append(tot_obj)
                    else:
                        messages.info(request, 'Invalid Request.')
                        return redirect("/logout")
                elif emp_desi in qa_list:
                    if type == 'all':
                        for i in campaign_list:
                            tot_obj = i.objects.filter(added_by=emp_id)
                            audits.append(tot_obj)
                    elif type == "fatal":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(added_by=emp_id, fatal=True,
                                                       audit_date__range=[month_start_date, todays_date])
                            audits.append(tot_obj)
                    elif type == "month":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(added_by=emp_id,
                                                       audit_date__range=[month_start_date, todays_date])
                            audits.append(tot_obj)
                    elif type == "open":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(added_by=emp_id, status=False)
                            audits.append(tot_obj)
                    elif type == "dispute":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(added_by=emp_id, dispute_status=True)
                            audits.append(tot_obj)
                    else:
                        messages.info(request, 'Invalid Request.')
                        return redirect("/logout")
                elif emp_desi == "Team Leader":
                    if type == 'all':
                        for i in campaign_list:
                            tot_obj = i.objects.filter(team_lead_id=emp_id)
                            audits.append(tot_obj)
                    elif type == "fatal":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(team_lead_id=emp_id, fatal=True,
                                                       audit_date__range=[month_start_date, todays_date])
                            audits.append(tot_obj)
                    elif type == "month":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(team_lead_id=emp_id,
                                                       audit_date__range=[month_start_date, todays_date])
                            audits.append(tot_obj)
                    elif type == "open":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(team_lead_id=emp_id, status=False)
                            audits.append(tot_obj)
                    elif type == "dispute":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(team_lead_id=emp_id, dispute_status=True)
                            audits.append(tot_obj)
                    else:
                        messages.info(request, 'Invalid Request.')
                        return redirect("/logout")
                elif emp_desi == "Assistant Manager":
                    if type == 'all':
                        for i in campaign_list:
                            tot_obj = i.objects.filter(am_id=emp_id)
                            audits.append(tot_obj)
                    elif type == "fatal":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(am_id=emp_id, fatal=True,
                                                       audit_date__range=[month_start_date, todays_date])
                            audits.append(tot_obj)
                    elif type == "month":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(am_id=emp_id, audit_date__range=[month_start_date, todays_date])
                            audits.append(tot_obj)
                    elif type == "open":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(am_id=emp_id, status=False)
                            audits.append(tot_obj)
                    elif type == "dispute":
                        for i in campaign_list:
                            tot_obj = i.objects.filter(am_id=emp_id, dispute_status=True)
                            audits.append(tot_obj)
                    else:
                        messages.info(request, 'Invalid Request.')
                        return redirect("/logout")
                else:
                    messages.warning(request, 'Invalid request. You have been Logged out!')
                    return redirect("/logout")
            else:
                if type == 'all':
                    for i in campaign_list:
                        tot_obj = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id)
                        audits.append(tot_obj)
                elif type == "fatal":
                    for i in campaign_list:
                        tot_obj = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id, fatal=True,
                                                   audit_date__range=[month_start_date, todays_date])
                        audits.append(tot_obj)
                elif type == "month":
                    for i in campaign_list:
                        tot_obj = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id,
                                                   audit_date__range=[month_start_date, todays_date])
                        audits.append(tot_obj)
                elif type == "open":
                    for i in campaign_list:
                        tot_obj = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id, status=False)
                        audits.append(tot_obj)
                elif type == "dispute":
                    for i in campaign_list:
                        tot_obj = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id, dispute_status=True)
                        audits.append(tot_obj)
                else:
                    messages.info(request, 'Invalid Request.')
                    return redirect("/logout")
            return audits

        audits = auditcalculator(type)
        data = {"audit": audits, "type": type, "qa_list": qa_list, "agent_list": agent_list, "mgr_list": mgr_list}
        return render(request, "agent_reports.html", data)
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


# Agent Report (agent-report)
@login_required
def agentReport(request):
    if request.method == "POST":
        id = request.POST["id"]
        type = request.POST["type"]

        for i in campaign_list:
            obj = i.objects.all()
            if obj.count() > 0:
                if obj[0].page_type == type:
                    audit = i.objects.get(id=id)
                    campaign = Campaign.objects.get(id=audit.campaign_id)
                    data = {"form": audit, 'campaign':campaign, "type": audit.campaign_type,
                            'agent_list': agent_list, 'mgr_list':mgr_list}
                    for j in pages:
                        if type == j:
                            return render(request, "agent/" + j + ".html", data)
                else:
                    pass
            else:
                pass

    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


# Agent Respond
@login_required
def agentRespond(request):
    now = date.today()
    if request.method == "POST":
        id = request.POST["id"]
        emp_com_accept = request.POST.get("emp_com_accept")
        emp_com_reject = request.POST.get("emp_com_reject")
        type = request.POST["type"]

        for i in campaign_list:
            obj = i.objects.all()
            if obj.count() > 0:
                if obj[0].campaign_type == type:
                    campaign = i
                else:
                    pass
            else:
                pass

        e = campaign.objects.get(id=id)

        if emp_com_accept:
            e.emp_comments = emp_com_accept
            e.status = True
            e.dispute_status = False
            e.closed_date = now
        if emp_com_reject:
            e.emp_comments = emp_com_reject
            e.status = False
            e.dispute_status = True
        e.save()
        messages.warning(request, 'Your response have been captured successfully!')
        return redirect("/agent-dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def IndividualReportView(request):
    designation = request.user.profile.emp_desi
    logged_emp_id = request.user.profile.emp_id
    if request.method == 'POST':
        emp_id = request.POST["emp_id"]
        emp_desi = Profile.objects.get(emp_id=emp_id).emp_desi
        profile = Profile.objects.get(emp_id=emp_id)

        if designation in mgr_list:
            if emp_desi in agent_list:
                # All Audits
                all_total_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(emp_id=emp_id).count()
                    all_total_count.append(campaign)
                all_total = 0
                for i in all_total_count:
                    all_total += i

                # All Audits Current Month

                # All Audits Current Month Count
                month_all_count = []
                for i in campaign_list:
                    camapign = i.objects.filter(emp_id=emp_id,
                                                audit_date__range=[month_start_date, todays_date]).count()
                    month_all_count.append(camapign)
                month_all_total = 0
                for i in month_all_count:
                    month_all_total += i

                # Month's Average Score
                camapign_score = 0
                for i in campaign_list:
                    score = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
                    for j in score:
                        camapign_score += j.overall_score
                if month_all_total == 0:
                    score_average = "No Audits This Month"
                else:
                    score_average = (camapign_score) / month_all_total

                # Month's Fatal Count
                fatal_count = 0
                for i in campaign_list:
                    fatal = i.objects.filter(emp_id=emp_id, audit_date__range=[month_start_date, todays_date])
                    for j in fatal:
                        fatal_count += j.fatal_count

                # Open Audits
                open_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(emp_id=emp_id, status=False).count()
                    open_count.append(campaign)
                open_total = 0
                for i in open_count:
                    open_total += i

                # Dispute Audits
                dispute_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(emp_id=emp_id, dispute_status=True).count()
                    dispute_count.append(campaign)
                dispute_total = 0
                for i in dispute_count:
                    dispute_total += i

                # Fatal Audits
                fatal_audit_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(emp_id=emp_id, fatal=True,
                                                audit_date__range=[month_start_date, todays_date]).count()
                    fatal_audit_count.append(campaign)
                fatal_total = 0
                for i in fatal_audit_count:
                    fatal_total += i

                # Coaching Closure
                closure_count_list = []
                for i in campaign_list:
                    campaign = i.objects.filter(emp_id=emp_id, status=True).count()
                    closure_count_list.append(campaign)
                closure_count = 0
                for i in closure_count_list:
                    closure_count += i

                if all_total == 0:
                    coaching_closure = "No Audits"
                else:
                    coaching_closure = (closure_count / all_total) * 100

                tot = []
                for i in campaign_list:
                    campaign = i.objects.filter(emp_id=emp_id, status=False)
                    tot.append(campaign)

                audits = []
                for i in campaign_list:
                    campaign = i.objects.filter(emp_id=emp_id).values("campaign").annotate(
                        score=Avg('overall_score'))
                    audits.append(campaign)
                new_audits = []
                for i in audits:
                    if i:
                        new_audits.append(i)

            elif emp_desi == "Team Leader":
                # All Audits
                all_total_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(team_lead_id=emp_id).count()
                    all_total_count.append(campaign)
                all_total = 0
                for i in all_total_count:
                    all_total += i

                # All Audits Current Month

                # All Audits Current Month Count
                month_all_count = []
                for i in campaign_list:
                    camapign = i.objects.filter(team_lead_id=emp_id,
                                                audit_date__range=[month_start_date, todays_date]).count()
                    month_all_count.append(camapign)
                month_all_total = 0
                for i in month_all_count:
                    month_all_total += i

                # Month's Average Score
                camapign_score = 0
                for i in campaign_list:
                    score = i.objects.filter(team_lead_id=emp_id, audit_date__range=[month_start_date, todays_date])
                    for j in score:
                        camapign_score += j.overall_score
                if month_all_total == 0:
                    score_average = "No Audits This Month"
                else:
                    score_average = (camapign_score) / month_all_total

                # Month's Fatal Count
                fatal_count = 0
                for i in campaign_list:
                    fatal = i.objects.filter(team_lead_id=emp_id, audit_date__range=[month_start_date, todays_date])
                    for j in fatal:
                        fatal_count += j.fatal_count

                # Open Audits
                open_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(team_lead_id=emp_id, status=False).count()
                    open_count.append(campaign)
                open_total = 0
                for i in open_count:
                    open_total += i

                # Dispute Audits
                dispute_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(team_lead_id=emp_id, dispute_status=True).count()
                    dispute_count.append(campaign)
                dispute_total = 0
                for i in dispute_count:
                    dispute_total += i

                # Fatal Audits
                fatal_audit_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(team_lead_id=emp_id, fatal=True,
                                                audit_date__range=[month_start_date, todays_date]).count()
                    fatal_audit_count.append(campaign)
                fatal_total = 0
                for i in fatal_audit_count:
                    fatal_total += i

                # Coaching Closure
                closure_count_list = []
                for i in campaign_list:
                    campaign = i.objects.filter(team_lead_id=emp_id, status=True).count()
                    closure_count_list.append(campaign)
                closure_count = 0
                for i in closure_count_list:
                    closure_count += i

                if all_total == 0:
                    coaching_closure = "No Audits"
                else:
                    coaching_closure = (closure_count / all_total) * 100

                tot = []
                for i in campaign_list:
                    campaign = i.objects.filter(team_lead_id=emp_id, status=False)
                    tot.append(campaign)

                audits = []
                for i in campaign_list:
                    campaign = i.objects.filter(team_lead_id=emp_id).values("campaign").annotate(
                        score=Avg('overall_score'))
                    audits.append(campaign)
                new_audits = []
                for i in audits:
                    if i:
                        new_audits.append(i)

            elif emp_desi in qa_list:
                # All Audits
                all_total_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(added_by=emp_id).count()
                    all_total_count.append(campaign)
                all_total = 0
                for i in all_total_count:
                    all_total += i

                # All Audits Current Month

                # All Audits Current Month Count
                month_all_count = []
                for i in campaign_list:
                    camapign = i.objects.filter(added_by=emp_id,
                                                audit_date__range=[month_start_date, todays_date]).count()
                    month_all_count.append(camapign)
                month_all_total = 0
                for i in month_all_count:
                    month_all_total += i

                # Month's Average Score
                camapign_score = 0
                for i in campaign_list:
                    score = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date])
                    for j in score:
                        camapign_score += j.overall_score
                if month_all_total == 0:
                    score_average = "No Audits This Month"
                else:
                    score_average = (camapign_score) / month_all_total

                # Month's Fatal Count
                fatal_count = 0
                for i in campaign_list:
                    fatal = i.objects.filter(added_by=emp_id, audit_date__range=[month_start_date, todays_date])
                    for j in fatal:
                        fatal_count += j.fatal_count

                # Open Audits
                open_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(added_by=emp_id, status=False).count()
                    open_count.append(campaign)
                open_total = 0
                for i in open_count:
                    open_total += i

                # Dispute Audits
                dispute_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(added_by=emp_id, dispute_status=True).count()
                    dispute_count.append(campaign)
                dispute_total = 0
                for i in dispute_count:
                    dispute_total += i

                # Fatal Audits
                fatal_audit_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(added_by=emp_id, fatal=True,
                                                audit_date__range=[month_start_date, todays_date]).count()
                    fatal_audit_count.append(campaign)
                fatal_total = 0
                for i in fatal_audit_count:
                    fatal_total += i

                # Coaching Closure
                closure_count_list = []
                for i in campaign_list:
                    campaign = i.objects.filter(added_by=emp_id, status=True).count()
                    closure_count_list.append(campaign)
                closure_count = 0
                for i in closure_count_list:
                    closure_count += i

                if all_total == 0:
                    coaching_closure = "No Audits"
                else:
                    coaching_closure = (closure_count / all_total) * 100

                tot = []
                for i in campaign_list:
                    campaign = i.objects.filter(added_by=emp_id, status=False)
                    tot.append(campaign)

                audits = []
                for i in campaign_list:
                    campaign = i.objects.filter(added_by=emp_id).values("campaign").annotate(
                        score=Avg('overall_score'))
                    audits.append(campaign)
                new_audits = []
                for i in audits:
                    if i:
                        new_audits.append(i)

            elif emp_desi == "Assistant Manager":
                # All Audits
                all_total_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(am_id=emp_id).count()
                    all_total_count.append(campaign)
                all_total = 0
                for i in all_total_count:
                    all_total += i

                # All Audits Current Month

                # All Audits Current Month Count
                month_all_count = []
                for i in campaign_list:
                    camapign = i.objects.filter(am_id=emp_id, audit_date__range=[month_start_date, todays_date]).count()
                    month_all_count.append(camapign)
                month_all_total = 0
                for i in month_all_count:
                    month_all_total += i

                # Month's Average Score
                camapign_score = 0
                for i in campaign_list:
                    score = i.objects.filter(am_id=emp_id, audit_date__range=[month_start_date, todays_date])
                    for j in score:
                        camapign_score += j.overall_score
                if month_all_total == 0:
                    score_average = "No Audits This Month"
                else:
                    score_average = (camapign_score) / month_all_total

                # Month's Fatal Count
                fatal_count = 0
                for i in campaign_list:
                    fatal = i.objects.filter(am_id=emp_id, audit_date__range=[month_start_date, todays_date])
                    for j in fatal:
                        fatal_count += j.fatal_count

                # Open Audits
                open_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(am_id=emp_id, status=False).count()
                    open_count.append(campaign)
                open_total = 0
                for i in open_count:
                    open_total += i

                # Dispute Audits
                dispute_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(am_id=emp_id, dispute_status=True).count()
                    dispute_count.append(campaign)
                dispute_total = 0
                for i in dispute_count:
                    dispute_total += i

                # Fatal Audits
                fatal_audit_count = []
                for i in campaign_list:
                    campaign = i.objects.filter(am_id=emp_id, fatal=True,
                                                audit_date__range=[month_start_date, todays_date]).count()
                    fatal_audit_count.append(campaign)
                fatal_total = 0
                for i in fatal_audit_count:
                    fatal_total += i

                # Coaching Closure
                closure_count_list = []
                for i in campaign_list:
                    campaign = i.objects.filter(am_id=emp_id, status=True).count()
                    closure_count_list.append(campaign)
                closure_count = 0
                for i in closure_count_list:
                    closure_count += i

                if all_total == 0:
                    coaching_closure = "No Audits"
                else:
                    coaching_closure = (closure_count / all_total) * 100

                tot = []
                for i in campaign_list:
                    campaign = i.objects.filter(am_id=emp_id, status=False)
                    tot.append(campaign)

                audits = []
                for i in campaign_list:
                    campaign = i.objects.filter(am_id=emp_id).values("campaign").annotate(
                        score=Avg('overall_score'))
                    audits.append(campaign)
                new_audits = []
                for i in audits:
                    if i:
                        new_audits.append(i)

            else:
                messages.warning(request, 'Invalid request. You have been Logged out!')
                return redirect("/logout")

        else:
            # All Audits
            all_total_count = []
            for i in campaign_list:
                campaign = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id).count()
                all_total_count.append(campaign)
            all_total = 0
            for i in all_total_count:
                all_total += i

            # All Audits Current Month

            # All Audits Current Month Count
            month_all_count = []
            for i in campaign_list:
                camapign = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id,
                                            audit_date__range=[month_start_date, todays_date]).count()
                month_all_count.append(camapign)
            month_all_total = 0
            for i in month_all_count:
                month_all_total += i

            # Month's Average Score
            camapign_score = 0
            for i in campaign_list:
                score = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id,
                                         audit_date__range=[month_start_date, todays_date])
                for j in score:
                    camapign_score += j.overall_score
            if month_all_total == 0:
                score_average = "No Audits This Month"
            else:
                score_average = (camapign_score) / month_all_total

            # Month's Fatal Count
            fatal_count = 0
            for i in campaign_list:
                fatal = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id,
                                         audit_date__range=[month_start_date, todays_date])
                for j in fatal:
                    fatal_count += j.fatal_count

            # Open Audits
            open_count = []
            for i in campaign_list:
                campaign = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id, status=False).count()
                open_count.append(campaign)
            open_total = 0
            for i in open_count:
                open_total += i

            # Dispute Audits
            dispute_count = []
            for i in campaign_list:
                campaign = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id, dispute_status=True).count()
                dispute_count.append(campaign)
            dispute_total = 0
            for i in dispute_count:
                dispute_total += i

            # Fatal Audits
            fatal_audit_count = []
            for i in campaign_list:
                campaign = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id, fatal=True,
                                            audit_date__range=[month_start_date, todays_date]).count()
                fatal_audit_count.append(campaign)
            fatal_total = 0
            for i in fatal_audit_count:
                fatal_total += i

            # Coaching Closure
            closure_count_list = []
            for i in campaign_list:
                campaign = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id, status=True).count()
                closure_count_list.append(campaign)
            closure_count = 0
            for i in closure_count_list:
                closure_count += i

            if all_total == 0:
                coaching_closure = "No Audits"
            else:
                coaching_closure = (closure_count / all_total) * 100

            tot = []
            for i in campaign_list:
                campaign = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id, status=False)
                tot.append(campaign)

            audits = []
            for i in campaign_list:
                campaign = i.objects.filter(emp_id=emp_id, added_by=logged_emp_id).values("campaign").annotate(
                    score=Avg('overall_score'))
                audits.append(campaign)
            new_audits = []
            for i in audits:
                if i:
                    new_audits.append(i)

        data = {
            "audit": tot, "month_all_total": month_all_total, "open_total": open_total, "dispute_total": dispute_total,
            "average": score_average, "fatal": fatal_count,
            "all_total": all_total, "fatal_total": fatal_total, "coaching_closure": coaching_closure,
            "profile": profile, "audits": new_audits, "desig": emp_desi
        }
        return render(request, "individual_reports.html", data)
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def CampaignAgentReportView(request):
    designation = request.user.profile.emp_desi
    added = request.user.profile.emp_id
    if request.method == 'POST':
        emp_id = request.POST["emp_id"]
        emp_desi = Profile.objects.get(emp_id=emp_id).emp_desi
        campaign = request.POST["campaign"]
        if emp_desi in agent_list:
            for i in campaign_list:
                obj = i.objects.all()
                if obj.count() > 0:
                    if obj[0].campaign == campaign:
                        if designation in qa_list:
                            campaign = i.objects.filter(emp_id=emp_id, added_by=added)
                        else:
                            campaign = i.objects.filter(emp_id=emp_id)

            audits = campaign
        elif emp_desi in qa_list:
            for i in campaign_list:
                obj = i.objects.all()
                if obj.count() > 0:
                    if obj[0].campaign == campaign:
                        if designation in qa_list:
                            campaign = i.objects.filter(added_by=emp_id)
                        else:
                            campaign = i.objects.filter(added_by=emp_id)
            audits = campaign
        type = "campaign"
        data = {"audit": audits, "type": type, "qa_list": qa_list, "agent_list": agent_list, "mgr_list": mgr_list}
        return render(request, "campaign_reports.html", data)
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def change_password_new(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            user = request.user
            user.profile.pc = True
            user.save()
            user.profile.save()
            messages.success(request, 'Your password was successfully updated! Please login with new password.')
            return redirect('/logout')
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('/change-password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'change-password.html', {'form': form, "agent": agent_list})


@login_required
def AddEmail(request):
    designation = request.user.profile.emp_desi
    if request.method == "POST":
        emp_id = request.POST["emp_id"]
        email = request.POST["email"]
        e = Profile.objects.get(emp_id=emp_id)
        e.emp_email = email
        e.save()
        messages.info(request, "Email Added Successfully !")
        return redirect("/dashboard")
    else:
        messages.info(request, 'Please add your Email ID')
        return render(request, "add-email.html")


@login_required
def EditEmail(request):
    designation = request.user.profile.emp_desi
    if request.method == "POST":
        emp_id = request.POST["emp_id"]
        email = request.POST["new_email"]
        e = Profile.objects.get(emp_id=emp_id)
        e.emp_email = email
        e.save()
        messages.info(request, "Email Changed Successfully !")
        return redirect("/dashboard")
    else:
        messages.info(request, "Invalid Request. You have been logged out :)")
        return redirect("/logout")


@login_required
def exportData(request):
    designation = request.user.profile.emp_desi
    emp_id = request.user.profile.emp_id
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        id = request.POST['campaign']
        campaign_type = Campaign.objects.get(id=id).type

        ######  Export Function #############
        def exportOutbound(monform):
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Employee ID', 'Associate Name', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact', 'Call Date', 'Call Duration ', 'Audit Date', 'Quality Analyst',
                           'Team Lead',
                           'Manager', 'Assistant Manager', 'Week',

                           'Used Standard Opening Protocol',
                           'Introduction of Product / Branding',
                           'Call Closing as per the Protocol',

                           'Followed Hold Procedure Appropriately/Dead Air',
                           'Used Empathetic Statements whenever required',
                           'Clear Grammar & Communication',
                           'Acknowledged Appropriately',
                           'Active Listening without Interruption',

                           'Followed Policy & Procedure (Script)',
                           'Probing/Tactful finding/Rebuttal',
                           'Accurate Documentation',
                           'Disposition done correctly',
                           'Inaccurate Information',
                           'Advisor Sounding Rude / Proafinity Usage',
                           "Compliance Total", "Total Score",
                           'Status', 'Dispute Status', 'Closed Date', 'Fatal', 'Fatal Count',
                           "Areas of improvement", "Positives", "Comments"]
            else:
                columns = ['Process/Campaign', 'Employee ID', 'Associate Name', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact', 'Call Date', 'Call Duration ', 'Audit Date', 'Quality Analyst',
                           'Team Lead',
                           'Manager', 'Assistant Manager', 'Week',

                           'Used Standard Opening Protocol',
                           'Introduction of Product / Branding',
                           'Call Closing as per the Protocol',

                           'Followed Hold Procedure Appropriately/Dead Air',
                           'Used Empathetic Statements whenever required',
                           'Clear Grammar & Communication',
                           'Acknowledged Appropriately',
                           'Active Listening without Interruption',

                           'Followed Policy & Procedure (Script)',
                           'Probing/Tactful finding/Rebuttal',
                           'Accurate Documentation',
                           'Disposition done correctly',
                           'Inaccurate Information',
                           'Advisor Sounding Rude / Proafinity Usage',
                           "Compliance Total", "Total Score",
                           'Status', 'Dispute Status', 'Closed Date', 'Fatal', 'Fatal Count',
                           "Areas of improvement", "Positives", "Comments", "Audit Duration"]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = monform.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id
                                              ).values_list(
                    'campaign', 'emp_id', 'associate_name', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'oc_1', 'oc_2', 'oc_3',
                    'softskill_1', 'softskill_2', 'softskill_3', 'softskill_4', 'softskill_5',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5', 'compliance_6',
                    "compliance_total", "overall_score",
                    'status', 'dispute_status', 'closed_date', 'fatal', 'fatal_count',
                    'areas_improvement', 'positives', 'comments')
            else:
                rows = monform.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'emp_id', 'associate_name', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'oc_1', 'oc_2', 'oc_3',
                    'softskill_1', 'softskill_2', 'softskill_3', 'softskill_4', 'softskill_5',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5', 'compliance_6',
                    "compliance_total", "overall_score",
                    'status', 'dispute_status', 'closed_date', 'fatal', 'fatal_count',
                    'areas_improvement', 'positives', 'comments', str("audit_duration"))

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response

        def exportInbound(monform):
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact',
                           'Call Date', 'Call Duration ', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           'Used Standard Opening Protocol',
                           'Personalization ( Report Building, Addressing by Name)',
                           'Acknowledged Appropriately',
                           'Active Listening without Interruption / Paraphrasing',
                           'Used Empathetic Statements whenever required',
                           'Clear Grammar / Sentence Structure',
                           'Tone & Intonation / Rate of Speech',
                           'Diction/ Choice of Words / Phrase',
                           'Took Ownership on the call',
                           'Followed Hold Procedure Appropriately / Dead Air',
                           'Offered Additional Assistance & Closed Call as per Protocol',

                           'Probing / Tactful Finding / Rebuttal',
                           'Complete Information Provided',

                           'Professional / Courtesy',
                           'Verification process followed',
                           'Case Study',
                           'Process & Procedure Followed',
                           'First Call Resolution',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total", "Total Score",
                           'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact',
                           'Call Date', 'Call Duration ', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           'Used Standard Opening Protocol',
                           'Personalization ( Report Building, Addressing by Name)',
                           'Acknowledged Appropriately',
                           'Active Listening without Interruption / Paraphrasing',
                           'Used Empathetic Statements whenever required',
                           'Clear Grammar / Sentence Structure',
                           'Tone & Intonation / Rate of Speech',
                           'Diction/ Choice of Words / Phrase',
                           'Took Ownership on the call',
                           'Followed Hold Procedure Appropriately / Dead Air',
                           'Offered Additional Assistance & Closed Call as per Protocol',

                           'Probing / Tactful Finding / Rebuttal',
                           'Complete Information Provided',

                           'Professional / Courtesy',
                           'Verification process followed',
                           'Case Study',
                           'Process & Procedure Followed',
                           'First Call Resolution',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total", "Total Score",
                           'Dispute Status', 'Areas of improvement', 'Positives', 'Comments', "Audit Duration"]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = monform.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id
                                              ).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date',
                    'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'ce_1', 'ce_2', 'ce_3', 'ce_4', 'ce_5', 'ce_6', 'ce_7', 'ce_8', 'ce_9', 'ce_10', 'ce_11',
                    'business_1', 'business_2',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments'
                )
            else:
                rows = monform.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date',
                    'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'ce_1', 'ce_2', 'ce_3', 'ce_4', 'ce_5', 'ce_6', 'ce_7', 'ce_8', 'ce_9', 'ce_10', 'ce_11',
                    'business_1', 'business_2',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments', "audit_duration"

                )

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        def exportEmail(monform):
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact', 'am', 'team_lead', 'manager', 'customer_name', 'customer_contact',
                           'Call Date', 'Call Duration ', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           'Associate used the standard greeting format',
                           'Appropriate responses ( acknowledging at the right time)',
                           'Ownership on Emails / Chat Answered within 30 Seconds',
                           'Personalization ( building a Report, Addressing by name)',
                           'Empathy/Sympathy',
                           'Sentence structure',
                           'Punctuation (full stop, comma, and brackets, used in writing to separate sentences)',
                           'Grammar (Tense, Noun, etc.)',
                           'Probing done whenever necessary',
                           'Recap (Summarization of the conversation)',
                           'Associate used the standard closing format',

                           'Accurate Resolution/Information is provided as per the process',
                           'Worked on the Ticket Assigned / Chat Responded within 5 mins',

                           'Professional / Courtesy',
                           'Verification process followed',
                           'Case Study',
                           'Process & Procedure Followed',
                           'First Chat / Email Resolution',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total", "Total Score",
                           'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact', 'am', 'team_lead', 'manager', 'customer_name', 'customer_contact',
                           'Call Date', 'Call Duration ', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           'Associate used the standard greeting format',
                           'Appropriate responses ( acknowledging at the right time)',
                           'Ownership on Emails / Chat Answered within 30 Seconds',
                           'Personalization ( building a Report, Addressing by name)',
                           'Empathy/Sympathy',
                           'Sentence structure',
                           'Punctuation (full stop, comma, and brackets, used in writing to separate sentences)',
                           'Grammar (Tense, Noun, etc.)',
                           'Probing done whenever necessary',
                           'Recap (Summarization of the conversation)',
                           'Associate used the standard closing format',

                           'Accurate Resolution/Information is provided as per the process',
                           'Worked on the Ticket Assigned / Chat Responded within 5 mins',

                           'Professional / Courtesy',
                           'Verification process followed',
                           'Case Study',
                           'Process & Procedure Followed',
                           'First Chat / Email Resolution',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total", "Total Score",
                           'Dispute Status', 'Areas of improvement', 'Positives', 'Comments', 'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = monform.objects.filter(
                    audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'team_lead', 'manager', 'customer_name',
                    'customer_contact',
                    'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'ce_1', 'ce_2', 'ce_3', 'ce_4', 'ce_5', 'ce_6',
                    'ce_7', 'ce_8', 'ce_9', 'ce_10', 'ce_11',
                    'business_1', 'business_2',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments')
            else:
                rows = monform.objects.filter(
                    audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'team_lead', 'manager', 'customer_name',
                    'customer_contact', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'ce_1', 'ce_2', 'ce_3', 'ce_4',
                    'ce_5', 'ce_6', 'ce_7', 'ce_8', 'ce_9', 'ce_10', 'ce_11',
                    'business_1', 'business_2',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status', 'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

        ########## Outbound Campaigns ##############
        if campaign_type == 'Outbound':
            response = exportOutbound(Outbound)
            return response

        ########## Inbound Campaigns ##############
        elif campaign_type == 'Inbound':
            response = exportInbound(Inbound)
            return response

        ########## Email/Chat Campaigns ##############
        elif campaign_type == 'Email / Chat':
            response = exportEmail(EmailChat)
            return response

        ########## Blazing Hog Campaign ##############
        elif campaign_type == 'Blazing Hog':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Email/Chat date',
                           'Ticket Id', 'Query Type', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           "Understanding and Solved Customer's Issue",
                           "Displayed process knowledge",
                           'Documentation - Full information captured in internal spreadsheet',
                           'Did the agent mention correct and adequate notes if necessary',

                           'Resolved/Assigned Ticket issue in a timely manner',
                           'Categorized case properly/Check other Tickets & Previous communition Merged',

                           'Assigned to the correct department',
                           'Tool usage',
                           'Edited Customer profile/Check customer profile',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Email/Chat date',
                           'Ticket Id', 'Query Type', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           "Understanding and Solved Customer's Issue",
                           "Displayed process knowledge",
                           'Documentation - Full information captured in internal spreadsheet',
                           'Did the agent mention correct and adequate notes if necessary',

                           'Resolved/Assigned Ticket issue in a timely manner',
                           'Categorized case properly/Check other Tickets & Previous communition Merged',

                           'Assigned to the correct department',
                           'Tool usage',
                           'Edited Customer profile/Check customer profile',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = BlazingHog.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'email_chat_date',
                    'ticket_id', 'query_type', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'solution_1', 'solution_2', 'solution_3', 'solution_4',
                    'efficiency_1', 'efficiency_2',
                    'compliance_1', 'compliance_2', 'compliance_3',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_score', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments')
            else:
                rows = BlazingHog.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'email_chat_date',
                    'ticket_id', 'query_type', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'solution_1', 'solution_2', 'solution_3', 'solution_4',
                    'efficiency_1', 'efficiency_2',
                    'compliance_1', 'compliance_2', 'compliance_3',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_score', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        ########## AB Hindalco Campaign ##############
        elif campaign_type == 'AB Hindalco':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact', 'Call Date', 'Call Duration ',
                           'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager', 'Assistant Manager', 'Week',

                           'Used Standard Opening Protocol',
                           'Introduction of Product / Branding - 4 USP of eternia - WiWA, Warranty, Duranium, Eternia care Mentioning Hindalco, Aditya birla group',
                           'Call Closing as per the Protocol',

                           'Used Empathetic Statements whenever required',
                           'Making the conversation 2 ways, giving chance to the customer to ask question',
                           'Active Listening without Interruption',
                           'Clear Grammar & Communication',

                           'Followed Policy & Procedure (Script)',
                           'Accurate Documentation with full details in ZOHO',
                           'Inaccurate Information : Identifying the right lead to opportunity',
                           'Advisor Sounding Rude / Proafinity Usage',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']

            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact', 'Call Date', 'Call Duration ',
                           'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager', 'Assistant Manager', 'Week',

                           'Used Standard Opening Protocol',
                           'Introduction of Product / Branding - 4 USP of eternia - WiWA, Warranty, Duranium, Eternia care Mentioning Hindalco, Aditya birla group',
                           'Call Closing as per the Protocol',

                           'Used Empathetic Statements whenever required',
                           'Making the conversation 2 ways, giving chance to the customer to ask question',
                           'Active Listening without Interruption',
                           'Clear Grammar & Communication',

                           'Followed Policy & Procedure (Script)',
                           'Accurate Documentation with full details in ZOHO',
                           'Inaccurate Information : Identifying the right lead to opportunity',
                           'Advisor Sounding Rude / Proafinity Usage',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = AbHindalco.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration',
                    'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'oc_1', 'oc_2', 'oc_3',
                    'softskill_1', 'softskill_2', 'softskill_3', 'softskill_4',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status', 'areas_improvement', 'positives', 'comments')
            else:
                rows = AbHindalco.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'oc_1', 'oc_2', 'oc_3',
                    'softskill_1', 'softskill_2', 'softskill_3', 'softskill_4',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments', 'audit_duration')
            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        ########## Digital Swiss Gold Campaign ##############
        elif campaign_type == 'Digital Swiss Gold':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact',
                           'Call Date', 'Call Duration ', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           'Associate used the standard greeting format',
                           'Appropriate responses ( acknowledging at the right time)',
                           'Ownership on Emails / Chat Answered within 30 Seconds',
                           'Personalization ( building a Raport, Addressing by name)',
                           'Empathy/Sympathy',
                           'Sentence structure',
                           'Punctuation (full stop, comma, and brackets, used in writing to separate sentences)',
                           'Grammar (Tense, Noun, etc.)',
                           'Probing done whenever necessary',
                           'Recap (Summarization of the conversation)',
                           'Associate used the standard closing format',

                           'Accurate Resolution/Information is provided as per the process',
                           'Worked on the Ticket Assigned / Chat Responded within 5 mins',

                           'Professional / Courtesy',
                           'Follow up done on the Pending Tickets (Chats & Email)',
                           'Refund / Retruns / Escalation Updated in the google sheet',
                           'Process & Procedure Followed',
                           'First Chat / Email Resolution',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",

                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments'
                           ]

            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact',
                           'Call Date', 'Call Duration ', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           'Associate used the standard greeting format',
                           'Appropriate responses ( acknowledging at the right time)',
                           'Ownership on Emails / Chat Answered within 30 Seconds',
                           'Personalization ( building a Raport, Addressing by name)',
                           'Empathy/Sympathy',
                           'Sentence structure',
                           'Punctuation (full stop, comma, and brackets, used in writing to separate sentences)',
                           'Grammar (Tense, Noun, etc.)',
                           'Probing done whenever necessary',
                           'Recap (Summarization of the conversation)',
                           'Associate used the standard closing format',

                           'Accurate Resolution/Information is provided as per the process',
                           'Worked on the Ticket Assigned / Chat Responded within 5 mins',

                           'Professional / Courtesy',
                           'Follow up done on the Pending Tickets (Chats & Email)',
                           'Refund / Retruns / Escalation Updated in the google sheet',
                           'Process & Procedure Followed',
                           'First Chat / Email Resolution',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",

                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments',
                           'Audit Duration'
                           ]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = DigitalSwissGold.objects.filter(audit_date__range=[start_date, end_date],
                                                       added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager''am', 'week',
                    'ce_1', 'ce_2', 'ce_3', 'ce_4', 'ce_5', 'ce_6', 'ce_7', 'ce_8', 'ce_9', 'ce_10', 'ce_11',
                    'business_1', 'business_2',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status', 'areas_improvement', 'positives', 'comments')
            else:
                rows = DigitalSwissGold.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager''am', 'week',
                    'ce_1', 'ce_2', 'ce_3', 'ce_4', 'ce_5', 'ce_6', 'ce_7', 'ce_8', 'ce_9', 'ce_10', 'ce_11',
                    'business_1', 'business_2',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status', 'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        ########## Noom EVA Campaign ##############
        elif campaign_type == 'Noom EVA':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Team Lead',
                           'Ticket Number', 'Concept',
                           'Transaction Handled Date', 'Evaluator Name', 'Week', 'Audit Date', 'Manager',
                           'Assistant Manager',

                           'If the user is missed to hit "finish" after sending the respective response. If the response is added with unwanted space and Punctuation. If the user name is miss-spelled/alphanumeric name on dashboard,we should use “Hey there!”.',
                           'If the "You last checked in" user is not sent with respective message or sent twice with the response',
                           'If the user are not assigned in spreadsheet. Ex: If the user code is not added in the spreadsheet.',
                           'If "was assigned to you" users are not hit finish',

                           "If a user's query is missed to answer and directly assigned to GS.",
                           'If the user is directly assigned without an Acknowledgement. If the user is sent with irrelevant response. If user is missed to assign to a coach while user wish to be assigned',
                           'If the response is sent with any irrelevant words or free handed messages. If the task is popped up as UU and YLCI the UU task should be our first priority',
                           'If the user has a System generated message of cancellation and CRO assigned to next GS. Negative empathy for user’s message!',
                           'If the user is missed to send the survey response and assigned directly. If the survey messages are swapped.',
                           'If the user has a question or information about Covid, that needs to addressed to coaches or Seek a help from the slack channels and then respond to it',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",

                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Team Lead',
                           'Ticket Number', 'Concept',
                           'Transaction Handled Date', 'Evaluator Name', 'Week', 'Audit Date', 'Manager',
                           'Assistant Manager',

                           'If the user is missed to hit "finish" after sending the respective response. If the response is added with unwanted space and Punctuation. If the user name is miss-spelled/alphanumeric name on dashboard,we should use “Hey there!”.',
                           'If the "You last checked in" user is not sent with respective message or sent twice with the response',
                           'If the user are not assigned in spreadsheet. Ex: If the user code is not added in the spreadsheet.',
                           'If "was assigned to you" users are not hit finish',

                           "If a user's query is missed to answer and directly assigned to GS.",
                           'If the user is directly assigned without an Acknowledgement. If the user is sent with irrelevant response. If user is missed to assign to a coach while user wish to be assigned',
                           'If the response is sent with any irrelevant words or free handed messages. If the task is popped up as UU and YLCI the UU task should be our first priority',
                           'If the user has a System generated message of cancellation and CRO assigned to next GS. Negative empathy for user’s message!',
                           'If the user is missed to send the survey response and assigned directly. If the survey messages are swapped.',
                           'If the user has a question or information about Covid, that needs to addressed to coaches or Seek a help from the slack channels and then respond to it',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",

                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = NoomEva.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'team_lead', 'ticket_number', 'concept',
                    'transaction_handled_date',
                    'evaluator_name', 'week', 'audit_date', 'manager', 'am',

                    'ce_1', 'ce_2', 'ce_3', 'ce_4',

                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5', 'compliance_6',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments')

            else:
                rows = NoomEva.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'team_lead', 'ticket_number', 'concept',
                    'transaction_handled_date',
                    'evaluator_name', 'week', 'audit_date', 'manager', 'am',

                    'ce_1', 'ce_2', 'ce_3', 'ce_4',

                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5', 'compliance_6',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        ########## FLA Campaign ##############
        elif campaign_type == 'FLA':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Team Lead',
                           'Manager',
                           'Assistant Manager', 'Week', 'Transaction Handled Date', 'Audit Date', 'Service', 'Order ID',
                           'Concept',
                           'Check List Used Correctly',
                           'Reason for Failure',
                           'Status', 'Closed Date', 'Fatal', 'Fatal Count',
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']

            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Team Lead',
                           'Manager',
                           'Assistant Manager', 'Week', 'Transaction Handled Date', 'Audit Date', 'Service', 'Order ID',
                           'Concept',
                           'Check List Used Correctly',
                           'Reason for Failure',
                           'Status', 'Closed Date', 'Fatal', 'Fatal Count',
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives',
                           'Comments', 'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = FLA.objects.filter(
                    audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'transaction_handles_date', 'audit_date', 'service', 'order_id', 'concept',

                    'check_list',
                    'reason_for_failure',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'overall_score', 'dispute_status',
                    'areas_improvement', 'positives', 'comments')
            else:
                rows = FLA.objects.filter(
                    audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',
                    'transaction_handles_date', 'audit_date', 'service', 'order_id', 'concept',

                    'check_list',
                    'reason_for_failure',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'overall_score', 'dispute_status',
                    'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
            return response

        ########## Fame House Campaign ##############
        elif campaign_type == 'Fame House':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Quality Analyst', 'Assistant Manager', 'Employee ID',
                           'Team Lead', 'Week', 'Transaction Date', 'Ticket Type', 'Audit Date', 'Ticket Number',

                           'Shipping product incorrectly',
                           'Incorrect grammar and spelling being used/illegible responses/Does not make sense.',
                           'Blatantly incorrect or made up information provided to the customer',
                           'Sending internal notes as Public response',
                           'Responding to any ticket outside of representatives skills/assignments',
                           'Unprofessional- tone,language or content. Uses derogatory language or curse words.',
                           'Not escalating a situation/Not following proper escalation procedure/Responding to an escalated ticket',
                           'Responding to Spam',
                           'Double response-w/o addressing and apologizing',
                           'Responding with personal opinions outside of company policy',
                           'Sending same macro as last agent w/o edits.',

                           'Agent sent response as public reply',

                           'Agent greeted customer by correct name',
                           'Agent used correct appreciation/acknowledgement statement',

                           'Agent composed email with logical flow that makes sense',
                           'Agent presented information with clear formatting, correct spelling and grammar',

                           'Agent chose correct macro(s).',
                           "Agent tailored macro(s) to fit the customer's question or issue",

                           'Agent asked the customer if he/she could be of additional help',
                           'Agent used appropriate closing & signature',

                           'Agent correctly identified and understood customer issue and responded accordingly (Issue Identification)',
                           'Agent fully resolved inquiry/issue upon first contact when possible, or clearly communicated additional information/next steps for full resolution. (Issue Resolution)',
                           'Agent did not deflect any questions/avoid policy communications unnecessarily. (Non-avoidance)',
                           'Agent conveyed correct policy information to the customer',
                           'Agent conveyed correct product information to the customer',
                           'Agent established correct timeline to resolution/ CSR did not delay resolution. (Resolution Timeline)',
                           'Rep fully and accurately helped the customer within their empowerments or escalated appropriately. (Agent Empowerments)',

                           "Agent validated the customer's concern / questions / reason for contacting us",
                           "Agent offered genuine acknowledgement and empathy for customer's concern",
                           'Agent used positive tone and impartial language in all communications',
                           'Agent was professional and courteous',
                           "Representative answered in a tone consistent with UMG's core values and culture",

                           'Agent accurately completed all necessary field on the ticket',
                           'Agent merged tickets properly',
                           'Agent performed all needed Shopify processes and accurately relayed all needed information and screenshots to customer.',
                           'Agent completed all system processes correctly',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",

                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Associate Name', 'Quality Analyst', 'Assistant Manager', 'Employee ID',
                           'Team Lead', 'Week', 'Transaction Date', 'Ticket Type', 'Audit Date', 'Ticket Number',

                           'Shipping product incorrectly',
                           'Incorrect grammar and spelling being used/illegible responses/Does not make sense.',
                           'Blatantly incorrect or made up information provided to the customer',
                           'Sending internal notes as Public response',
                           'Responding to any ticket outside of representatives skills/assignments',
                           'Unprofessional- tone,language or content. Uses derogatory language or curse words.',
                           'Not escalating a situation/Not following proper escalation procedure/Responding to an escalated ticket',
                           'Responding to Spam',
                           'Double response-w/o addressing and apologizing',
                           'Responding with personal opinions outside of company policy',
                           'Sending same macro as last agent w/o edits.',

                           'Agent sent response as public reply',

                           'Agent greeted customer by correct name',
                           'Agent used correct appreciation/acknowledgement statement',

                           'Agent composed email with logical flow that makes sense',
                           'Agent presented information with clear formatting, correct spelling and grammar',

                           'Agent chose correct macro(s).',
                           "Agent tailored macro(s) to fit the customer's question or issue",

                           'Agent asked the customer if he/she could be of additional help',
                           'Agent used appropriate closing & signature',

                           'Agent correctly identified and understood customer issue and responded accordingly (Issue Identification)',
                           'Agent fully resolved inquiry/issue upon first contact when possible, or clearly communicated additional information/next steps for full resolution. (Issue Resolution)',
                           'Agent did not deflect any questions/avoid policy communications unnecessarily. (Non-avoidance)',
                           'Agent conveyed correct policy information to the customer',
                           'Agent conveyed correct product information to the customer',
                           'Agent established correct timeline to resolution/ CSR did not delay resolution. (Resolution Timeline)',
                           'Rep fully and accurately helped the customer within their empowerments or escalated appropriately. (Agent Empowerments)',

                           "Agent validated the customer's concern / questions / reason for contacting us",
                           "Agent offered genuine acknowledgement and empathy for customer's concern",
                           'Agent used positive tone and impartial language in all communications',
                           'Agent was professional and courteous',
                           "Representative answered in a tone consistent with UMG's core values and culture",

                           'Agent accurately completed all necessary field on the ticket',
                           'Agent merged tickets properly',
                           'Agent performed all needed Shopify processes and accurately relayed all needed information and screenshots to customer.',
                           'Agent completed all system processes correctly',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",

                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = FameHouse.objects.filter(audit_date__range=[start_date, end_date],
                                                added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'quality_analyst', 'am', 'emp_id', 'team_lead', 'week', 'trans_date',
                    'ticket_type', 'audit_date', 'ticket_no',

                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5', 'compliance_6',
                    'compliance_7', 'compliance_8', 'compliance_9', 'compliance_10', 'compliance_11',

                    'cr_1',

                    'opening_1', 'opening_2',

                    'comp_1', 'comp_2',

                    'macro_1', 'macro_2',

                    'closing_1', 'closing_2',

                    'cir_1', 'cir_2', 'cir_3', 'cir_4', 'cir_5', 'cir_6', 'cir_7',

                    'et_1', 'et_2', 'et_3', 'et_4', 'et_5',

                    'doc_1', 'doc_2', 'doc_3', 'doc_4',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status', 'areas_improvement', 'positives', 'comments')
            else:
                rows = FameHouse.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'quality_analyst', 'am', 'emp_id', 'team_lead', 'week', 'trans_date',
                    'ticket_type', 'audit_date', 'ticket_no',

                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5',
                    'compliance_6', 'compliance_7', 'compliance_8', 'compliance_9', 'compliance_10', 'compliance_11',

                    'cr_1',

                    'opening_1', 'opening_2',

                    'comp_1', 'comp_2',

                    'macro_1', 'macro_2',

                    'closing_1', 'closing_2',

                    'cir_1', 'cir_2', 'cir_3', 'cir_4', 'cir_5', 'cir_6', 'cir_7',

                    'et_1', 'et_2', 'et_3', 'et_4', 'et_5',

                    'doc_1', 'doc_2', 'doc_3', 'doc_4',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        ########## Noom POD Campaign ##############
        elif campaign_type == 'Noom pod':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Team Lead',
                           'Ticket Number', 'Concept', 'Transaction Handled Date', 'Evaluator Name', 'Week',
                           'Audit Date',
                           'Manager', 'Assistant Manager',

                           'If the Messages are switched around. i,e Second message sent in the place of first message. If the task is not been cleared. If the user name is in alphanumeric then it should be used as "Hey there". If the canned response is sent twise. The CRO should make sure that #SCI 1 (FCI) is reflecting on task list. Make sure only one task due today is on the task list.',
                           'In YLCI ,second message is sent in the place of first message. Any unnecessary space in the FCI canned response will be a NCE.',
                           'In YLCI If the user is missed to Receive respective response for the SGM {Thanks for sticking in with noom}.',
                           'In YLCI if user receives the message twice. If user is missed to hit finish the task after sending the message.',

                           'If the user receive irrespective message instead of respective message I.e., sending GCI message instead of FCI message. Only first name of the user should be sent with canned message. If there is any personal reply from the user that Particular users should be Skipped.',
                           'If the user’s message was sent After or equal to 14 days irrespective of any task, those users should to be skipped to UU auto generate. Else if any irrelevant response is sent for a user.',
                           'If the user’s last message be like UU response those users should be mark as inactive or skip. If the last messages looks like an acknowledgement for a UU response, those users should be skipped or Mark as inactive.',
                           'If any "Task due today" is popped up with YLC, that user need to be sent with appropriate "Task due today" canned message. If the TDT is repeated on task list with a different date and time or different task those users needs to be skipped.',
                           'User should be sent with the response which is loaded on Canned response list, make sure not to add any extra contents in it! If the user is skipped without a valid reason.',
                           'In Group posting if the content/image is missed in post. If the content/Image is swapped.',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total", "Total Score",
                           'Dispute Status',
                           'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Team Lead',
                           'Ticket Number',
                           'Concept', 'Transaction Handled Date', 'Evaluator Name', 'Week', 'Audit Date', 'Manager',
                           'Assistant Manager',

                           'If the Messages are switched around. i,e Second message sent in the place of first message. If the task is not been cleared. If the user name is in alphanumeric then it should be used as "Hey there". If the canned response is sent twise. The CRO should make sure that #SCI 1 (FCI) is reflecting on task list. Make sure only one task due today is on the task list.',
                           'In YLCI ,second message is sent in the place of first message. Any unnecessary space in the FCI canned response will be a NCE.',
                           'In YLCI If the user is missed to Receive respective response for the SGM {Thanks for sticking in with noom}.',
                           'In YLCI if user receives the message twice. If user is missed to hit finish the task after sending the message.',

                           'If the user receive irrespective message instead of respective message I.e., sending GCI message instead of FCI message. Only first name of the user should be sent with canned message. If there is any personal reply from the user that Particular users should be Skipped.',
                           'If the user’s message was sent After or equal to 14 days irrespective of any task, those users should to be skipped to UU auto generate. Else if any irrelevant response is sent for a user.',
                           'If the user’s last message be like UU response those users should be mark as inactive or skip. If the last messages looks like an acknowledgement for a UU response, those users should be skipped or Mark as inactive.',
                           'If any "Task due today" is popped up with YLC, that user need to be sent with appropriate "Task due today" canned message. If the TDT is repeated on task list with a different date and time or different task those users needs to be skipped.',
                           'User should be sent with the response which is loaded on Canned response list, make sure not to add any extra contents in it! If the user is skipped without a valid reason.',
                           'In Group posting if the content/image is missed in post. If the content/Image is swapped.',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Compliance Total",

                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = NoomPod.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'team_lead', 'ticket_number', 'concept',
                    'transaction_handled_date', 'evaluator_name', 'week', 'audit_date', 'manager', 'am',
                    'ce_1', 'ce_2', 'ce_3', 'ce_4',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5', 'compliance_6',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status', 'areas_improvement', 'positives', 'comments')
            else:
                rows = NoomPod.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'team_lead', 'ticket_number', 'concept',
                    'transaction_handled_date', 'evaluator_name', 'week', 'audit_date', 'manager', 'am',
                    'ce_1', 'ce_2', 'ce_3', 'ce_4',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4', 'compliance_5', 'compliance_6',
                    'status', 'closed_date', 'fatal', 'fatal_count', 'compliance_total', 'overall_score',
                    'dispute_status', 'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        ########## Practo Campaign ##############
        elif campaign_type == 'Practo':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Employee ID', 'Associate Name', 'Chat Date', 'Case Number/Chat Link',
                           'Issue Type', 'Sub-Issue Type', 'Sub Sub-Issue Type',
                           'CSAT', 'Product', 'Audit Date', 'Quality Analyst', 'Assistant Manager',
                           'Team Lead',
                           'Manager', 'Week', 'Zone', 'Concept',

                           'Chat Closing',
                           "Failed to close the chat",
                           "Failed to use the standard script (survey)",
                           "Multiple closing statement used",
                           "Failed to offer further assistance",
                           "User ended the chat",
                           "NA",
                           'FRTAT',
                           'Addressing the user/Personalisation of chat',
                           "No Attempt",
                           "First name used on the chat",
                           "Less attempt - More scope",
                           "Failed to probe the user name",
                           'Incorrect Salutation',
                           "NA",
                           "Assistance & Acknowledgment",
                           "No Attempt",
                           'First name used on the chat',
                           'Less attempt - More scope',
                           "Failed to probe the user name",
                           "Incorrect Salutation",
                           "NA",
                           'Relevant responses',
                           "Assurance",
                           "Probing",
                           "Irrelevant Probing",
                           "Incomplete Probing",
                           "Didn't Attempt to Probe",
                           'NA',
                           "Interaction: Empathy , Profressional, care",
                           "No Empathy",
                           "Lack of Professionalism",
                           "Lack of Care",
                           'Lack of Empathy',
                           "Inappropriate empathy",
                           "Repetitive empathy statement",
                           'NA',
                           'Grammar',
                           "Punctuation",
                           "Capitalization",
                           "Typing Error",
                           "Sentence Formation",
                           "Spacing",
                           "NA",
                           "Being courteous & using plesantries",
                           "Process followed",
                           'SOP has not followed',
                           'Incorrect Information',
                           'Incomplete Information',
                           'Failed to authenticate for the medicine order',
                           "Incorrect TAT (or) Failed to inform the TAT",
                           "Incomplete/Incorrect refund details and wrong redirection",
                           'NA',
                           'Explanation Skills (Being Specific, Reasoning) & Rebuttal Handling',
                           "Sharing the information in a sequential manner",
                           "Case Documentation",
                           "Curation",
                           'Incomplete',
                           "Inappropriate",
                           "NA",
                           "Average Speed of Answer",
                           'Chat Hold Procedure &: Taking Permission before putting the chat on hold.',
                           "Standard script not used",
                           "Failed to refresh the chat within promised time.",
                           "Failed to retrieve the chat",
                           "NA",
                           "PE knowledge base adherence",
                           "Failed to refer the knowledge base",
                           "Referred, but not confident",
                           "Incorrect category referred by the agent",
                           "NA",
                           "Expectations: Setting correct expectations about issue resolution",
                           "Incomplete Resolution",
                           "Incorrect Resolution",
                           "Process breach",
                           "ZTP(Zero Tolerance Policy)",

                           'status', 'Dispute Status', 'Total Score', 'Closed Date', 'Fatal', 'Fatal Count',
                           'Areas of improvement', 'Specific Reason for FATAL with Labels and Sub Label', 'Comments']
            else:
                columns = ['Process/Campaign', 'Employee ID', 'Associate Name', 'Chat Date', 'Case Number/Chat Link',
                           'Issue Type', 'Sub-Issue Type', 'Sub Sub-Issue Type',
                           'CSAT', 'Product', 'Audit Date', 'Quality Analyst', 'Assistant Manager',
                           'Team Lead',
                           'Manager', 'Week', 'Zone', 'Concept',

                           'Chat Closing',
                           "Failed to close the chat",
                           "Failed to use the standard script (survey)",
                           "Multiple closing statement used",
                           "Failed to offer further assistance",
                           "User ended the chat",
                           "NA",
                           'FRTAT',
                           'Addressing the user/Personalisation of chat',
                           "No Attempt",
                           "First name used on the chat",
                           "Less attempt - More scope",
                           "Failed to probe the user name",
                           'Incorrect Salutation',
                           "NA",
                           "Assistance & Acknowledgment",
                           "No Attempt",
                           'First name used on the chat',
                           'Less attempt - More scope',
                           "Failed to probe the user name",
                           "Incorrect Salutation",
                           "NA",
                           'Relevant responses',
                           "Assurance",
                           "Probing",
                           "Irrelevant Probing",
                           "Incomplete Probing",
                           "Didn't Attempt to Probe",
                           'NA',
                           "Interaction: Empathy , Profressional, care",
                           "No Empathy",
                           "Lack of Professionalism",
                           "Lack of Care",
                           'Lack of Empathy',
                           "Inappropriate empathy",
                           "Repetitive empathy statement",
                           'NA',
                           'Grammar',
                           "Punctuation",
                           "Capitalization",
                           "Typing Error",
                           "Sentence Formation",
                           "Spacing",
                           "NA",
                           "Being courteous & using plesantries",
                           "Process followed",
                           'SOP has not followed',
                           'Incorrect Information',
                           'Incomplete Information',
                           'Failed to authenticate for the medicine order',
                           "Incorrect TAT (or) Failed to inform the TAT",
                           "Incomplete/Incorrect refund details and wrong redirection",
                           'NA',
                           'Explanation Skills (Being Specific, Reasoning) & Rebuttal Handling',
                           "Sharing the information in a sequential manner",
                           "Case Documentation",
                           "Curation",
                           'Incomplete',
                           "Inappropriate",
                           "NA",
                           "Average Speed of Answer",
                           'Chat Hold Procedure &: Taking Permission before putting the chat on hold.',
                           "Standard script not used",
                           "Failed to refresh the chat within promised time.",
                           "Failed to retrieve the chat",
                           "NA",
                           "PE knowledge base adherence",
                           "Failed to refer the knowledge base",
                           "Referred, but not confident",
                           "Incorrect category referred by the agent",
                           "NA",
                           "Expectations: Setting correct expectations about issue resolution",
                           "Incomplete Resolution",
                           "Incorrect Resolution",
                           "Process breach",
                           "ZTP(Zero Tolerance Policy)",

                           'status', 'Dispute Status', 'Total Score', 'Closed Date', 'Fatal', 'Fatal Count',
                           'Areas of improvement', 'Specific Reason for FATAL with Labels and Sub Label', 'Comments',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = Practo.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'emp_id', 'associate_name', 'chat_date', 'case_no', 'issue_type', 'sub_issue',
                    'sub_sub_issue',
                    'csat',
                    'product', 'audit_date', 'quality_analyst ', 'am', 'team_lead', 'manager', 'week', 'zone',
                    'concept',

                    'p_1', 'p1_s1', 'p1_s2', 'p1_s3', 'p1_s4', 'p1_s5', 'p1_s6', 'p_2', 'p_3', 'p3_s1', 'p3_s2',
                    'p3_s3',
                    'p3_s4', 'p3_s5', 'p3_s6', 'p_4', 'p4_s1', 'p4_s2', 'p4_s3', 'p4_s4', 'p4_s5', 'p_5', 'p_6', 'p_7',
                    'p7_s1', 'p7_s2', 'p7_s3', 'p7_s4', 'p_8', 'p8_s1', 'p8_s2', 'p8_s3', 'p8_s4', 'p8_s5', 'p8_s6',
                    'p8_s7', 'p_9', 'p9_s1', 'p9_s2', 'p9_s3', 'p9_s4', 'p9_s5', 'p9_s6', 'p_10', 'p_11', 'p11_s1',
                    'p11_s2', 'p11_s3', 'p11_s4', 'p11_s5', 'p11_s6', 'p11_s7', 'p_12', 'p_13', 'p_14', 'p_15',
                    'p15_s1',
                    'p15_s2', 'p15_s3', 'p_16', 'p_17', 'p17_s1', 'p17_s2', 'p17_s3', 'p17_s4', 'p_18', 'p18_s1',
                    'p18_s2', 'p18_s3', 'p18_s4', 'compliance_1', 'compliance1_s1', 'compliance1_s2', 'compliance1_s3',
                    'compliance_2',

                    'status', 'disput_status', 'overall_score',
                    'closed_date', 'fatal', 'fatal_count', 'areas_improvement', 'positives', 'comments')
            else:
                rows = Practo.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'emp_id', 'associate_name', 'chat_date', 'case_no', 'issue_type', 'sub_issue',
                    'sub_sub_issue',
                    'csat',
                    'product', 'audit_date', 'quality_analyst ', 'am', 'team_lead', 'manager', 'week', 'zone',
                    'concept',

                    'p_1', 'p1_s1', 'p1_s2', 'p1_s3', 'p1_s4', 'p1_s5', 'p1_s6', 'p_2', 'p_3', 'p3_s1', 'p3_s2',
                    'p3_s3',
                    'p3_s4', 'p3_s5', 'p3_s6', 'p_4', 'p4_s1', 'p4_s2', 'p4_s3', 'p4_s4', 'p4_s5', 'p_5', 'p_6', 'p_7',
                    'p7_s1', 'p7_s2', 'p7_s3', 'p7_s4', 'p_8', 'p8_s1', 'p8_s2', 'p8_s3', 'p8_s4', 'p8_s5', 'p8_s6',
                    'p8_s7', 'p_9', 'p9_s1', 'p9_s2', 'p9_s3', 'p9_s4', 'p9_s5', 'p9_s6', 'p_10', 'p_11', 'p11_s1',
                    'p11_s2', 'p11_s3', 'p11_s4', 'p11_s5', 'p11_s6', 'p11_s7', 'p_12', 'p_13', 'p_14', 'p_15',
                    'p15_s1',
                    'p15_s2', 'p15_s3', 'p_16', 'p_17', 'p17_s1', 'p17_s2', 'p17_s3', 'p17_s4', 'p_18', 'p18_s1',
                    'p18_s2', 'p18_s3', 'p18_s4', 'compliance_1', 'compliance1_s1', 'compliance1_s2', 'compliance1_s3',
                    'compliance_2',

                    'status', 'disput_status', 'overall_score',
                    'closed_date', 'fatal', 'fatal_count', 'areas_improvement', 'positives', 'comments',
                    'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response

        ########## Winopoly Campaign ##############
        elif campaign_type == 'Winopoly Outbound':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Customer Name',
                           'Team Lead', 'Customer Contact', 'Call Date', 'Zone', 'Call Duration', 'Audit Date',
                           'Concept',
                           'Disposition', 'Manager', 'Assistant Manager', 'Week',

                           'Recording Disclosure - (Agent must disclose the call is recorded)',
                           'Rep Name - (Did agent introduce her/himself during opening?)',
                           'Branding/Site Name - (Did the agent state the site name name in the opening?)',
                           'Call Reason - (Did the agent state the reason for the call? (confirmation call))',
                           'Contact Information - (Did the agent verify the contact info?)',

                           'Targeted Spotlight offer - (Did the agent attempt the Targeted spotlight offer?)',
                           'Lead offer - (Did the agent attempt the lead offer?)',
                           'Verification - (Did the agent ask all verification questions were applicaple?)',

                           'Excessisive off topic conversations - (Did the agent avoid unnessesary off topic conversations)',
                           'Polite - (Follow up done on the Pending Tickets (Chats & Email))',
                           'Positive and Upbeat - (Did the agent have a positive and upbeat tone)',
                           'Ethics - (Did the agent advoid misleading information about offers)',
                           'Call control - (Did the agent take control of the call)',
                           'Program of Interest - (Did the agent match the lead to a program that they stated interest in, without having to push the lead into agreeing to the program?)',

                           'TCPA Close - (Did the rep read a TCPA statement and receive an affirmative response from the lead (Yes or Yeah)?)',
                           'TCPA Close - (If interrupted did the agent reread the TCPA and get an affimative response)',
                           'Do Not Call Request - (Agent followed DNC Request Policy)',
                           'California Privacy Policy - (Agent followed CA Policy Privacy by reading the written statement for CA residents)',
                           'Transfering the call - (Did the agent conduct the intro on the transfer correctly?)',
                           'Transfer Only - (Did the agent conduct the intro on the transfer correctly)',
                           'Disposition - (Did the agent used the correct disposition?)',
                           'Auto Fail - (ZERO TOLERANCE POLICY)',
                           'Status', 'Dispute Status',
                           'Closed Date', 'Fatal', 'Fatal Count' 'EVALUATORS COMMENT', 'COACHING COMMENTS']

            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Customer Name',
                           'Team Lead', 'Customer Contact', 'Call Date', 'Zone', 'Call Duration', 'Audit Date',
                           'Concept',
                           'Disposition', 'Manager', 'Assistant Manager', 'Week',
                           'Recording Disclosure - (Agent must disclose the call is recorded)',
                           'Rep Name - (Did agent introduce her/himself during opening?)',
                           'Branding/Site Name - (Did the agent state the site name name in the opening?)',
                           'Call Reason - (Did the agent state the reason for the call? (confirmation call))',
                           'Contact Information - (Did the agent verify the contact info?)',

                           'Targeted Spotlight offer - (Did the agent attempt the Targeted spotlight offer?)',
                           'Lead offer - (Did the agent attempt the lead offer?)',
                           'Verification - (Did the agent ask all verification questions were applicaple?)',

                           'Excessisive off topic conversations - (Did the agent avoid unnessesary off topic conversations)',
                           'Polite - (Follow up done on the Pending Tickets (Chats & Email))',
                           'Positive and Upbeat - (Did the agent have a positive and upbeat tone)',
                           'Ethics - (Did the agent advoid misleading information about offers)',
                           'Call control - (Did the agent take control of the call)',
                           'Program of Interest - (Did the agent match the lead to a program that they stated interest in, without having to push the lead into agreeing to the program?)',

                           'TCPA Close - (Did the rep read a TCPA statement and receive an affirmative response from the lead (Yes or Yeah)?)',
                           'TCPA Close - (If interrupted did the agent reread the TCPA and get an affimative response)',
                           'Do Not Call Request - (Agent followed DNC Request Policy)',
                           'California Privacy Policy - (Agent followed CA Policy Privacy by reading the written statement for CA residents)',
                           'Transfering the call - (Did the agent conduct the intro on the transfer correctly?)',
                           'Transfer Only - (Did the agent conduct the intro on the transfer correctly)',
                           'Disposition - (Did the agent used the correct disposition?)',
                           'Auto Fail - (ZERO TOLERANCE POLICY)',
                           'Status', 'Dispute Status',
                           'Closed Date', 'Fatal', 'Fatal Count' 'EVALUATORS COMMENT', 'COACHING COMMENTS',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = Winopoly.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'customer_name', 'team_lead',
                    'customer_contact', 'call_date',
                    'zone', 'call_duration', 'audit_date', 'concept', 'disposition', 'manager', 'am', 'week',
                    'comp_1', 'op_2', 'op_3', 'op_4', 'op_5',
                    'mp_1', 'mp_2', 'mp_3',
                    'cp_1', 'cp_2', 'cp_3', 'cp_4', 'cp_5', 'cp_6',
                    'comp_2', 'comp_3', 'comp_4', 'comp_5',
                    'tp_1', 'tp_2', 'tp_3', 'comp_6',
                    'status', 'dispute_status', 'closed_date', 'fatal', 'fatal_count', 'evaluator_comment',
                    'coaching_comments')

            else:
                rows = Winopoly.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'customer_name', 'team_lead',
                    'customer_contact', 'call_date', 'zone', 'call_duration', 'audit_date', 'concept', 'disposition',
                    'manager', 'am', 'week',
                    'comp_1', 'op_2', 'op_3', 'op_4', 'op_5',
                    'mp_1', 'mp_2', 'mp_3',
                    'cp_1', 'cp_2', 'cp_3', 'cp_4', 'cp_5', 'cp_6',
                    'comp_2', 'comp_3', 'comp_4', 'comp_5',
                    'tp_1', 'tp_2', 'tp_3', 'comp_6',
                    'status', 'dispute_status', 'closed_date', 'fatal', 'fatal_count', 'evaluator_comment',
                    'coaching_comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row
                    in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        ########## ILM Campaign ##############
        elif campaign_type == 'IL Makiage':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Customer Name',
                           'Team Lead',
                           'Ticket ID', 'Email/Chat date', 'Zone', 'Assistant Manager', 'Audit Date', 'Concept', 'Week',
                           'Query Type',

                           "Understanding and Solved Customer's Issue",
                           'Gave alternatives when required/applicable & Displayed expert product knowledge',
                           'Coupon code added/Edited Name/Values & Date//Personalised when applicable',
                           'Answered all question effectively',
                           'Resolved issue in a timely manner',
                           'Categorized case properly/Check other Tickets &Previous communition Merged',
                           'Appropriate use of macros',
                           'Magento was utilized correctly',
                           'Identified correct order type',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Total Score",
                           'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Associate Name', 'Employee ID', 'Quality Analyst', 'Customer Name',
                           'Team Lead',
                           'Ticket ID', 'Email/Chat date', 'Zone', 'Assistant Manager', 'Audit Date', 'Concept', 'Week',
                           'Query Type',

                           "Understanding and Solved Customer's Issue",
                           'Gave alternatives when required/applicable & Displayed expert product knowledge',
                           'Coupon code added/Edited Name/Values & Date//Personalised when applicable',
                           'Answered all question effectively',
                           'Resolved issue in a timely manner',
                           'Categorized case properly/Check other Tickets &Previous communition Merged',
                           'Appropriate use of macros',
                           'Magento was utilized correctly',
                           'Identified correct order type',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', "Total Score",
                           'Dispute Status', 'Areas of improvement', 'Positives', 'Comments', 'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = ILMakiage.objects.filter(
                    audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'customer_name', 'team_lead',
                    'ticket_id',
                    'email_chat_date', 'zone', 'am', 'audit_date', 'concept', 'week', 'query_type',

                    's_1', 's_2', 's_3', 's_4',

                    'e_1', 'e_2',

                    'compliance_1', 'compliance_2', 'compliance_3',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'overall_score', 'dispute_status',
                    'areas_improvement', 'positives', 'comments')
            else:
                rows = ILMakiage.objects.filter(
                    audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'associate_name', 'emp_id', 'quality_analyst', 'customer_name', 'team_lead',
                    'ticket_id',
                    'email_chat_date', 'zone', 'am', 'audit_date', 'concept', 'week', 'query_type',

                    's_1', 's_2', 's_3', 's_4',

                    'e_1', 'e_2',

                    'compliance_1', 'compliance_2', 'compliance_3',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'overall_score', 'dispute_status',
                    'areas_improvement',
                    'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response

        elif campaign_type == 'Spoiled Child':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Employee ID', 'Associate Name', 'Zone', 'Customer Name', 'Concept',
                           'Email Chat Date', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager',
                           'Week',

                           "Understanding and Solved Customer's Issue?",
                           "Gave alternatives when required/applicable & displayed expert product knowledge?",
                           'Coupon code added/Edited Name/Values & Date//Personalized when applicable?',
                           'Answered all question effectively?',

                           "Resolved issue in a timely manner?",
                           'Categorized case properly/Check other Tickets &Previous commination Merged?',

                           'Appropriate use of macros?',
                           'Magento was utilized correctly?',
                           'Identified correct order type ?',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', 'Solution Score', 'Efficiency Score',
                           "Compliance Total",
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Employee ID', 'Associate Name', 'Zone', 'Customer Name', 'Concept',
                           'Email Chat Date', 'Audit Date', 'Quality Analyst', 'Team Lead', 'Manager',
                           'Assistant Manager',
                           'Week',

                           "Understanding and Solved Customer's Issue?",
                           "Gave alternatives when required/applicable & displayed expert product knowledge?",
                           'Coupon code added/Edited Name/Values & Date//Personalized when applicable?',
                           'Answered all question effectively?',

                           "Resolved issue in a timely manner?",
                           'Categorized case properly/Check other Tickets &Previous commination Merged?',

                           'Appropriate use of macros?',
                           'Magento was utilized correctly?',
                           'Identified correct order type ?',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', 'Solution Score', 'Efficiency Score',
                           "Compliance Total",
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = SpoiledChild.objects.filter(audit_date__range=[start_date, end_date],
                                                   added_by=emp_id).values_list(
                    'campaign', 'emp_id', 'associate_name', 'zone', 'customer_name', 'concept', 'email_chat_date',
                    'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',

                    'solution_1', 'solution_2', 'solution_3', 'solution_4',
                    'efficiency_1', 'efficiency_2',
                    'compliance_1', 'compliance_2', 'compliance_3',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'solution_score', 'efficiency_score',
                    'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments')
            else:
                rows = SpoiledChild.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'emp_id', 'associate_name', 'zone', 'customer_name', 'concept', 'email_chat_date',
                    'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',

                    'solution_1', 'solution_2', 'solution_3', 'solution_4',
                    'efficiency_1', 'efficiency_2',
                    'compliance_1', 'compliance_2', 'compliance_3',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'solution_score', 'efficiency_score',
                    'compliance_total', 'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        elif campaign_type == 'Nerotel Inbound':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="audit-report.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data
            # Sheet header, first row
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            if designation in qa_list:
                columns = ['Process/Campaign', 'Employee ID', 'Associate Name', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact', 'Call Date', 'Call Duration', 'Audit Date', 'Quality Analyst',
                           'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           "Greeting?",
                           "Value Proposition?",
                           'Tone and Pace?',
                           'Screening Questions?',
                           "How clear and concise was the rep's vocalization and pronunciation?",
                           'Did the rep use the correct hold procedure?',
                           'Providing Solutions?',
                           'Did the rep display active listening skills?',
                           'Call closure phase? Last Checks ?',

                           'Confirmation?',
                           'Preparation?',
                           'Clinic Procedures?',
                           'Did the rep manage time effectively?',

                           'Documentation?',
                           'Patient Details?',
                           'Discovery Questions? ',
                           'Was agent rude on the call?',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', 'Engagement Total', 'Resolution Total',
                           "Compliance Total",
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments']
            else:
                columns = ['Process/Campaign', 'Employee ID', 'Associate Name', 'Zone', 'Concept', 'Customer Name',
                           'Customer Contact', 'Call Date', 'Call Duration', 'Audit Date', 'Quality Analyst',
                           'Team Lead', 'Manager',
                           'Assistant Manager', 'Week',

                           "Greeting?",
                           "Value Proposition?",
                           'Tone and Pace?',
                           'Screening Questions?',
                           "How clear and concise was the rep's vocalization and pronunciation?",
                           'Did the rep use the correct hold procedure?',
                           'Providing Solutions?',
                           'Did the rep display active listening skills?',
                           'Call closure phase? Last Checks ?',

                           'Confirmation?',
                           'Preparation?',
                           'Clinic Procedures?',
                           'Did the rep manage time effectively?',

                           'Documentation?',
                           'Patient Details?',
                           'Discovery Questions? ',
                           'Was agent rude on the call?',

                           'Status', 'Closed Date', 'Fatal', 'Fatal Count', 'Engagement Total', 'Resolution Total',
                           "Compliance Total",
                           "Total Score", 'Dispute Status', 'Areas of improvement', 'Positives', 'Comments',
                           'Audit Duration']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            if designation in qa_list:
                rows = Nerotel.objects.filter(audit_date__range=[start_date, end_date], added_by=emp_id).values_list(
                    'campaign', 'emp_id', 'associate_name', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',

                    'eng_1', 'eng_2', 'eng_3', 'eng_4', 'eng_5', 'eng_6', 'eng_7', 'eng_8', 'eng_9',
                    'res_1', 'res_2', 'res_3', 'res_4',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'eng_total', 'res_total', 'compliance_total',
                    'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments')
            else:
                rows = Nerotel.objects.filter(audit_date__range=[start_date, end_date]).values_list(
                    'campaign', 'emp_id', 'associate_name', 'zone', 'concept', 'customer_name', 'customer_contact',
                    'call_date', 'call_duration', 'audit_date', 'quality_analyst', 'team_lead', 'manager', 'am', 'week',

                    'eng_1', 'eng_2', 'eng_3', 'eng_4', 'eng_5', 'eng_6', 'eng_7', 'eng_8', 'eng_9',
                    'res_1', 'res_2', 'res_3', 'res_4',
                    'compliance_1', 'compliance_2', 'compliance_3', 'compliance_4',

                    'status', 'closed_date', 'fatal', 'fatal_count', 'eng_total', 'res_total', 'compliance_total',
                    'overall_score',
                    'dispute_status',
                    'areas_improvement', 'positives', 'comments', 'audit_duration')

            rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in
                    rows]

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)

            return response

        return redirect("/dashboard")
    else:
        messages.info(request, "Invalid Request. You have been logged out :)")
        return redirect("/logout")


@login_required
def AddUser(request):
    designation = request.user.profile.emp_desi
    if designation in mgr_list:
        if request.method == 'POST':
            emp_id = request.POST['emp_id']
            emp_name = request.POST['emp_name']
            emp_email = request.POST.get('emp_email')
            emp_desi = request.POST['emp_desi']
            emp_pro = request.POST['emp_pro']
            emp_tl_id = request.POST['emp_tl']
            emp_tl = Profile.objects.get(emp_id=emp_tl_id).emp_name
            emp_am_id = request.POST['emp_am']
            emp_am = Profile.objects.get(emp_id=emp_am_id).emp_name
            emp_man_id = request.POST['emp_man']
            emp_man = Profile.objects.get(emp_id=emp_man_id).emp_name
            agent_status = "Active"

            admin_id = request.POST['admin_id']
            admin_pass = request.POST['admin_pass']

            if admin_id.casefold() == "admin" and admin_pass == "test":
                try:
                    User.objects.get(username=emp_id)
                    messages.info(request, "User not added because user with same Employee Id already Exists")
                    return redirect("/add-user")
                except User.DoesNotExist:
                    a = User.objects.create_user(username=emp_id, password=emp_id)
                    e = Profile()
                    e.user_id = a.id
                    e.emp_id = emp_id
                    e.emp_name = emp_name
                    if emp_email:
                        e.emp_email = emp_email
                    e.emp_desi = emp_desi
                    e.emp_process = emp_pro
                    e.emp_rm1 = emp_tl
                    e.emp_rm1_id = emp_tl_id
                    e.emp_rm2 = emp_am
                    e.emp_rm2_id = emp_am_id
                    e.emp_rm3 = emp_man
                    e.emp_rm3_id = emp_man_id
                    e.agent_status = agent_status
                    e.save()

                    messages.info(request, "The user has been added! The username and password is " + emp_id)
                    return redirect("/add-user")
            else:
                messages.info(request, "User Not Added. Invalid Admin Credentials :)")
                return redirect("/add-user")
        else:
            cam = Campaign.objects.all()
            profiles = Profile.objects.all().exclude(emp_desi__in=agent_list)
            data = {"campaigns": cam, "profiles": profiles}
            return render(request, "add_user.html", data)
    else:
        messages.info(request, "Invalid Request. You have been logged out :)")
        return redirect("/logout")


@login_required
def AddCampaign(request):
    emp_desi = request.user.profile.emp_desi
    if emp_desi in mgr_list:
        if request.method == 'POST':
            campaign = request.POST['cam_name']
            cam_type = request.POST['cam_type']
            threshold = request.POST['passing']

            if cam_type == "Outbound":
                page_type = "Outbound"
            elif cam_type == "Inbound":
                page_type = "Inbound"
            else:
                page_type = "Email"
            try:
                Campaign.objects.get(name__iexact=campaign, type=cam_type)
                messages.info(request, "Campaign With Same Name and Type is already Available!")
                return redirect("/add-campaign")
            except Campaign.DoesNotExist:
                e = Campaign()
                e.name = campaign
                e.type = cam_type
                e.page_type = page_type
                e.threshold = threshold
                e.save()
                messages.info(request, "Campaign Added Successfully !")
                return redirect("/add-campaign")
        else:
            return render(request, "add_campaign.html")
    else:
        messages.info(request, "Invalid Request. You have been logged out :)")
        return redirect("/logout")


@login_required
def AddQaMapping(request):
    emp_desi = request.user.profile.emp_desi
    if emp_desi in mgr_list:
        if request.method == 'POST':
            qa_id = request.POST['qa']
            campaign = request.POST['campaign']
            campaign = Campaign.objects.get(id=campaign)
            qa_name = Profile.objects.get(emp_id=qa_id).emp_name
            try:
                CampaignMapping.objects.get(qa_id=qa_id, campaign=campaign)
                messages.info(request, "QA already assigned to this campaign !")
                return redirect("/add-qa-mapping")
            except CampaignMapping.DoesNotExist:
                cam = CampaignMapping()
                cam.qa = qa_name
                cam.qa_id = qa_id
                cam.campaign = campaign
                cam.save()
                messages.info(request, "QA assigned Successfully !")
                return redirect("/view-qa-mapping")
        else:
            campaigns = Campaign.objects.all()
            qa = Profile.objects.filter(emp_desi__in=qa_list)
            data = {'campaigns': campaigns, 'qa': qa}
            return render(request, "add_qa_mapping.html", data)
    else:
        messages.info(request, "Invalid Request. You have been logged out :)")
        return redirect("/logout")


# View QA Mapping
@login_required
def viewQaMapping(request):
    campaigns = CampaignMapping.objects.all()
    qa = Profile.objects.filter(emp_desi__in=qa_list)
    data = {'campaigns': campaigns, 'qa': qa}
    return render(request, "view_qa_mapping.html", data)


# Delete QA Mapping
@login_required
def deleteQaMapping(request):
    if request.method == "POST":
        id = request.POST["id"]
        e = CampaignMapping.objects.get(id=id)
        e.delete()
        messages.info(request, "Mapping of deleted Successfully")
        return redirect("/view-qa-mapping")
    else:
        messages.info(request, "Invalid Request. You have been logged out :)")
        return redirect("/logout")


# Outbound Form Submit
@login_required
def outboundFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        opening_ques_1 = int(request.POST["oc_1"])
        opening_ques_2 = int(request.POST["oc_2"])
        opening_ques_3 = int(request.POST["oc_3"])
        openng_score = opening_ques_1 + opening_ques_2 + opening_ques_3

        softskills_ques_1 = int(request.POST["softskill_1"])
        softskills_ques_2 = int(request.POST["softskill_2"])
        softskills_ques_3 = int(request.POST["softskill_3"])
        softskills_ques_4 = int(request.POST["softskill_4"])
        softskills_ques_5 = int(request.POST["softskill_5"])
        softskill_score = softskills_ques_1 + softskills_ques_2 + softskills_ques_3 + softskills_ques_4 + softskills_ques_5

        business_compliance_qus_1 = int(request.POST["compliance_1"])
        business_compliance_qus_2 = int(request.POST["compliance_2"])
        business_compliance_qus_3 = int(request.POST["compliance_3"])
        business_compliance_qus_4 = int(request.POST["compliance_4"])
        business_compliance_qus_5 = int(request.POST["compliance_5"])
        business_compliance_qus_6 = int(request.POST["compliance_6"])
        business_compliance_score = business_compliance_qus_1 + business_compliance_qus_2 + business_compliance_qus_3 + business_compliance_qus_4 + business_compliance_qus_5 + business_compliance_qus_6

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [business_compliance_qus_1, business_compliance_qus_2, business_compliance_qus_3,
                      business_compliance_qus_4, business_compliance_qus_5, business_compliance_qus_6]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if business_compliance_qus_1 == 0 or business_compliance_qus_2 == 0 or business_compliance_qus_3 == 0 or business_compliance_qus_4 == 0 or business_compliance_qus_5 == 0 or business_compliance_qus_6 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = openng_score + softskill_score + business_compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = Outbound()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.oc_total = openng_score
        e.softskill_total = softskill_score
        e.compliance_total = business_compliance_score
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.oc_1 = opening_ques_1
        e.oc_2 = opening_ques_2
        e.oc_3 = opening_ques_3
        e.softskill_1 = softskills_ques_1
        e.softskill_2 = softskills_ques_2
        e.softskill_3 = softskills_ques_3
        e.softskill_4 = softskills_ques_4
        e.softskill_5 = softskills_ques_5
        e.compliance_1 = business_compliance_qus_1
        e.compliance_2 = business_compliance_qus_2
        e.compliance_3 = business_compliance_qus_3
        e.compliance_4 = business_compliance_qus_4
        e.compliance_5 = business_compliance_qus_5
        e.compliance_6 = business_compliance_qus_6
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)
        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


# Inbound Form Submit
@login_required
def inboundFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_5 = int(request.POST["ce_5"])
        ce_6 = int(request.POST["ce_6"])
        ce_7 = int(request.POST["ce_7"])
        ce_8 = int(request.POST["ce_8"])
        ce_9 = int(request.POST["ce_9"])
        ce_10 = int(request.POST["ce_10"])
        ce_11 = int(request.POST["ce_11"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4 + ce_5 + ce_6 + ce_7 + ce_8 + ce_9 + ce_10 + ce_11

        business_1 = int(request.POST["business_1"])
        business_2 = int(request.POST["business_2"])
        business_score = business_1 + business_2

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_score = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + business_score + compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = Inbound()
        e.audit_id = audit_id
        e.audit_duration = duration
        e.unique_id = unique_id
        e.ce_total = ce_total
        e.business_total = business_score
        e.compliance_total = compliance_score
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week

        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.ce_5 = ce_5
        e.ce_6 = ce_6
        e.ce_7 = ce_7
        e.ce_8 = ce_8
        e.ce_9 = ce_9
        e.ce_10 = ce_10
        e.ce_11 = ce_11

        e.business_1 = business_1
        e.business_2 = business_2

        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5

        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


# Email Form Submit
@login_required
def emailFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_5 = int(request.POST["ce_5"])
        ce_6 = int(request.POST["ce_6"])
        ce_7 = int(request.POST["ce_7"])
        ce_8 = int(request.POST["ce_8"])
        ce_9 = int(request.POST["ce_9"])
        ce_10 = int(request.POST["ce_10"])
        ce_11 = int(request.POST["ce_11"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4 + ce_5 + ce_6 + ce_7 + ce_8 + ce_9 + ce_10 + ce_11

        business_1 = int(request.POST["business_1"])
        business_2 = int(request.POST["business_2"])
        business_score = business_1 + business_2

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_score = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + business_score + compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = EmailChat()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.ce_total = ce_total
        e.business_total = business_score
        e.compliance_total = compliance_score
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week

        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.ce_5 = ce_5
        e.ce_6 = ce_6
        e.ce_7 = ce_7
        e.ce_8 = ce_8
        e.ce_9 = ce_9
        e.ce_10 = ce_10
        e.ce_11 = ce_11

        e.business_1 = business_1
        e.business_2 = business_2

        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5

        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def DigitalSwissGoldFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_5 = int(request.POST["ce_5"])
        ce_6 = int(request.POST["ce_6"])
        ce_7 = int(request.POST["ce_7"])
        ce_8 = int(request.POST["ce_8"])
        ce_9 = int(request.POST["ce_9"])
        ce_10 = int(request.POST["ce_10"])
        ce_11 = int(request.POST["ce_11"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4 + ce_5 + ce_6 + ce_7 + ce_8 + ce_9 + ce_10 + ce_11

        business_1 = int(request.POST["business_1"])
        business_2 = int(request.POST["business_2"])
        business_score = business_1 + business_2

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_score = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + business_score + compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = DigitalSwissGold()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.ce_total = ce_total
        e.business_total = business_score
        e.compliance_total = compliance_score
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week

        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.ce_5 = ce_5
        e.ce_6 = ce_6
        e.ce_7 = ce_7
        e.ce_8 = ce_8
        e.ce_9 = ce_9
        e.ce_10 = ce_10
        e.ce_11 = ce_11

        e.business_1 = business_1
        e.business_2 = business_2

        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5

        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def FLAFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]
        transaction_handles_date = request.POST["transdate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        service = request.POST["service"]
        order_id = request.POST["order_id"]

        check_list = int(request.POST["checklist_1"])

        reason_for_failure = request.POST["reason_for_failure"]
        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [check_list]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if check_list == 0:
            total_score = 0
            fatal = True
        else:
            total_score = check_list
            fatal = False
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = FLA()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.transaction_handles_date = transaction_handles_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.reason_for_failure = reason_for_failure
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.service = service
        e.order_id = order_id
        e.check_list = check_list
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def blazingHogFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]
        zone = request.POST["zone"]
        customer_name = request.POST["customer"]

        email_chat_date = request.POST["calldate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        query_type = request.POST["query_type"]
        ticket_id = request.POST["ticketnumber"]

        solution_1 = int(request.POST["solution_1"])
        solution_2 = int(request.POST["solution_2"])
        solution_3 = int(request.POST["solution_3"])
        solution_4 = int(request.POST["solution_4"])
        solution_score = solution_1 + solution_2 + solution_3 + solution_4
        efficiency_1 = int(request.POST["efficiency_1"])
        efficiency_2 = int(request.POST["efficiency_2"])
        efficiency_score = efficiency_1 + efficiency_2
        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_score = compliance_1 + compliance_2 + compliance_3

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = solution_score + efficiency_score + compliance_score
            fatal = False

        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = BlazingHog()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.email_chat_date = email_chat_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.zone = zone
        e.customer_name = customer_name
        e.query_type = query_type
        e.ticket_id = ticket_id
        e.solution_1 = solution_1
        e.solution_2 = solution_2
        e.solution_3 = solution_3
        e.solution_4 = solution_4
        e.efficiency_1 = efficiency_1
        e.efficiency_2 = efficiency_2
        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.solution_score = solution_score
        e.efficiency_score = efficiency_score
        e.compliance_score = compliance_score
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def NoomPodFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]

        transaction_handled_date = request.POST["transdate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        evaluator_name = request.POST["evaluator"]
        ticket_number = request.POST["ticketnumber"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_6 = int(request.POST["compliance_6"])
        compliance_total = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5 + compliance_6

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5, compliance_6]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0 or compliance_6 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + compliance_total
            fatal = False

        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = NoomPod()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.transaction_handled_date = transaction_handled_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.evaluator_name = evaluator_name
        e.ticket_number = ticket_number
        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5
        e.compliance_6 = compliance_6
        e.ce_total = ce_total
        e.compliance_total = compliance_total
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def NoomEvaFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]

        transaction_handled_date = request.POST["transdate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        evaluator_name = request.POST["evaluator"]
        ticket_number = request.POST["ticketnumber"]

        ce_1 = int(request.POST["ce_1"])
        ce_2 = int(request.POST["ce_2"])
        ce_3 = int(request.POST["ce_3"])
        ce_4 = int(request.POST["ce_4"])
        ce_total = ce_1 + ce_2 + ce_3 + ce_4

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_6 = int(request.POST["compliance_6"])
        compliance_total = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5 + compliance_6

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5, compliance_6]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0 or compliance_6 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = ce_total + compliance_total
            fatal = False

        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = NoomEva()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.transaction_handled_date = transaction_handled_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.evaluator_name = evaluator_name
        e.ticket_number = ticket_number
        e.ce_1 = ce_1
        e.ce_2 = ce_2
        e.ce_3 = ce_3
        e.ce_4 = ce_4
        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4
        e.compliance_5 = compliance_5
        e.compliance_6 = compliance_6
        e.ce_total = ce_total
        e.compliance_total = compliance_total
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def AbHindalcoFormSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]

        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        opening_ques_1 = int(request.POST["oc_1"])
        opening_ques_2 = int(request.POST["oc_2"])
        opening_ques_3 = int(request.POST["oc_3"])
        openng_score = opening_ques_1 + opening_ques_2 + opening_ques_3

        softskills_ques_1 = int(request.POST["softskill_1"])
        softskills_ques_2 = int(request.POST["softskill_2"])
        softskills_ques_3 = int(request.POST["softskill_3"])
        softskills_ques_4 = int(request.POST["softskill_4"])
        softskill_score = softskills_ques_1 + softskills_ques_2 + softskills_ques_3 + softskills_ques_4

        business_compliance_qus_1 = int(request.POST["compliance_1"])
        business_compliance_qus_2 = int(request.POST["compliance_2"])
        business_compliance_qus_3 = int(request.POST["compliance_3"])
        business_compliance_qus_4 = int(request.POST["compliance_4"])
        business_compliance_score = business_compliance_qus_1 + business_compliance_qus_2 + business_compliance_qus_3 + business_compliance_qus_4

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [opening_ques_2, business_compliance_qus_2, business_compliance_qus_3, business_compliance_qus_4]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if opening_ques_2 == 0 or business_compliance_qus_2 == 0 or business_compliance_qus_3 == 0 or business_compliance_qus_4 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = openng_score + softskill_score + business_compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = AbHindalco()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.oc_total = openng_score
        e.softskill_total = softskill_score
        e.compliance_total = business_compliance_score
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.oc_1 = opening_ques_1
        e.oc_2 = opening_ques_2
        e.oc_3 = opening_ques_3
        e.softskill_1 = softskills_ques_1
        e.softskill_2 = softskills_ques_2
        e.softskill_3 = softskills_ques_3
        e.softskill_4 = softskills_ques_4
        e.compliance_1 = business_compliance_qus_1
        e.compliance_2 = business_compliance_qus_2
        e.compliance_3 = business_compliance_qus_3
        e.compliance_4 = business_compliance_qus_4
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)
        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def PractoSubmit(request):
    if request.method == 'POST':
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type

        associate_name = request.POST['empname']
        emp_id = request.POST['empid']
        zone = request.POST['zone']
        concept = request.POST['concept']
        case_no = request.POST["case_no"]
        issue_type = request.POST["issue_type"]
        sub_issue_type = request.POST["sub_issue_type"]
        sub_sub_issue_type = request.POST["sub_sub_issue_type"]
        chat_date = request.POST["chat_date"]
        csat = request.POST['csat']
        product = request.POST['product']

        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        p_1 = int(request.POST['p1'])  # Chat Closing
        p1_s1 = request.POST.get("chat_1")
        p1_s2 = request.POST.get("chat_2")
        p1_s3 = request.POST.get("chat_3")
        p1_s4 = request.POST.get("chat_4")
        p1_s5 = request.POST.get("chat_5")
        p1_s6 = request.POST.get("chat_6")
        p_2 = int(request.POST['p2'])  # FRTAT
        p_3 = int(request.POST['p3'])  # Addressing the user/Personalisation of chat
        p3_s1 = request.POST.get("pers_1")
        p3_s2 = request.POST.get("pers_2")
        p3_s3 = request.POST.get("pers_3")
        p3_s4 = request.POST.get("pers_4")
        p3_s5 = request.POST.get("pers_5")
        p3_s6 = request.POST.get("pers_6")
        p_4 = int(request.POST['p4'])  # Assistance & Acknowledgment
        p4_s1 = request.POST.get("assu_1")
        p4_s2 = request.POST.get("assu_2")
        p4_s3 = request.POST.get("assu_3")
        p4_s4 = request.POST.get("assu_4")
        p4_s5 = request.POST.get("assu_5")
        p_5 = int(request.POST['p5'])  # Relevant responses
        p_6 = int(request.POST['p19'])  # Assurance
        p_7 = int(request.POST['p6'])  # Probing
        p7_s1 = request.POST.get("prob_1")
        p7_s2 = request.POST.get("prob_2")
        p7_s3 = request.POST.get("prob_3")
        p7_s4 = request.POST.get("prob_4")
        p_8 = int(request.POST['p7'])  # Interaction: Empathy , Profressional, care
        p8_s1 = request.POST.get("inte_1")
        p8_s2 = request.POST.get("inte_2")
        p8_s3 = request.POST.get("inte_3")
        p8_s4 = request.POST.get("inte_4")
        p8_s5 = request.POST.get("inte_5")
        p8_s6 = request.POST.get("inte_6")
        p8_s7 = request.POST.get("inte_7")
        p_9 = int(request.POST['p8'])  # Grammar
        p9_s1 = request.POST.get("gram_1")
        p9_s2 = request.POST.get("gram_2")
        p9_s3 = request.POST.get("gram_3")
        p9_s4 = request.POST.get("gram_4")
        p9_s5 = request.POST.get("gram_5")
        p9_s6 = request.POST.get("gram_6")
        p_10 = int(request.POST['p10'])  # Being courteous & using plesantries
        p_11 = int(request.POST['p11'])  # Process followed
        p11_s1 = request.POST.get("proc_1")
        p11_s2 = request.POST.get("proc_2")
        p11_s3 = request.POST.get("proc_3")
        p11_s4 = request.POST.get("proc_4")
        p11_s5 = request.POST.get("proc_5")
        p11_s6 = request.POST.get("proc_6")
        p11_s7 = request.POST.get("proc_7")
        p_12 = int(request.POST['p12'])  # Explanation Skills (Being Specific, Reasoning) & Rebuttal Handling
        p_13 = int(request.POST['p13'])  # Sharing the information in a sequential manner
        p_14 = int(request.POST['p14'])  # Case Documentation
        p_15 = int(request.POST['p15'])  # Curation
        p15_s1 = request.POST.get("cura_1")
        p15_s2 = request.POST.get("cura_2")
        p15_s3 = request.POST.get("cura_3")
        p_16 = int(request.POST['p16'])  # Average Speed of Answer
        p_17 = int(request.POST['p17'])  # Chat Hold Procedure &: Taking Permission before putting the chat on hold.
        p17_s1 = request.POST.get("hold_1")
        p17_s2 = request.POST.get("hold_3")
        p17_s3 = request.POST.get("hold_3")
        p17_s4 = request.POST.get("hold_4")
        p_18 = int(request.POST['p18'])  # PE knowledge base adherence
        p18_s1 = request.POST.get("pekb_1")
        p18_s2 = request.POST.get("pekb_2")
        p18_s3 = request.POST.get("pekb_3")
        p18_s4 = request.POST.get("pekb_4")

        # Score
        lst = lst = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, p_9, p_10, p_11, p_12, p_13, p_14, p_15, p_16, p_17, p_18]
        score = sum(lst)

        # Compliance
        compliance_1 = request.POST['fatal1']  # Expectations: Setting correct expectations about issue resolution
        compliance1_s1 = request.POST.get("expe_1")
        compliance1_s2 = request.POST.get("expe_2")
        compliance1_s3 = request.POST.get("expe_3")
        compliance_2 = request.POST['fatal2']  # ZTP(Zero Tolerance Policy)

        # Comments
        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 'fatal' or compliance_2 == 'fatal':
            total_score = 0
            fatal = True
        else:
            total_score = score
            fatal = False
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        try:
            Practo.objects.get(unique_id=unique_id)
            messages.info(request, "Please have patience! How ever the Audit has been Added :)")
            return redirect("/dashboard")
        except Practo.DoesNotExist:
            e = Practo()
            e.audit_id = audit_id
            e.unique_id = unique_id
            e.audit_duration = duration
            e.campaign = campaign_name
            e.campaign_type = campaign_type
            e.campaign_id = campaign_id
            e.chat_date = chat_date
            e.associate_name = associate_name
            e.emp_id = emp_id
            e.zone = zone
            e.concept = concept

            e.case_no = case_no
            e.issue_type = issue_type
            e.sub_issue = sub_issue_type
            e.sub_sub_issue = sub_sub_issue_type
            e.csat = csat
            e.product = product

            e.audit_date = audit_date
            e.quality_analyst = quality_analyst
            e.team_lead = team_lead
            e.manager = manager
            e.am = am
            e.team_lead_id = team_lead_id
            e.manager_id = manager_id
            e.am_id = am_id
            e.week = week

            e.p_1 = p_1
            e.p_2 = p_2
            e.p_3 = p_3
            e.p_4 = p_4
            e.p_5 = p_5
            e.p_6 = p_6
            e.p_7 = p_7
            e.p_8 = p_8
            e.p_9 = p_9
            e.p_10 = p_10
            e.p_11 = p_11
            e.p_12 = p_12
            e.p_13 = p_13
            e.p_14 = p_14
            e.p_15 = p_15
            e.p_16 = p_16
            e.p_17 = p_17
            e.p_18 = p_18
            e.p1_s1 = p1_s1
            e.p1_s2 = p1_s2
            e.p1_s3 = p1_s3
            e.p1_s4 = p1_s4
            e.p1_s5 = p1_s5
            e.p1_s6 = p1_s6
            e.p3_s1 = p3_s1
            e.p3_s2 = p3_s2
            e.p3_s3 = p3_s3
            e.p3_s4 = p3_s4
            e.p3_s5 = p3_s5
            e.p3_s6 = p3_s6
            e.p4_s1 = p4_s1
            e.p4_s2 = p4_s2
            e.p4_s3 = p4_s3
            e.p4_s4 = p4_s4
            e.p4_s5 = p4_s5
            e.p7_s1 = p7_s1
            e.p7_s2 = p7_s2
            e.p7_s3 = p7_s3
            e.p7_s4 = p7_s4
            e.p8_s1 = p8_s1
            e.p8_s2 = p8_s2
            e.p8_s3 = p8_s3
            e.p8_s4 = p8_s4
            e.p8_s5 = p8_s5
            e.p8_s6 = p8_s6
            e.p8_s7 = p8_s7
            e.p9_s1 = p9_s1
            e.p9_s2 = p9_s2
            e.p9_s3 = p9_s3
            e.p9_s4 = p9_s4
            e.p9_s5 = p9_s5
            e.p9_s6 = p9_s6
            e.p11_s1 = p11_s1
            e.p11_s2 = p11_s2
            e.p11_s3 = p11_s3
            e.p11_s4 = p11_s4
            e.p11_s5 = p11_s5
            e.p11_s6 = p11_s6
            e.p11_s7 = p11_s7
            e.p15_s1 = p15_s1
            e.p15_s2 = p15_s2
            e.p15_s3 = p15_s3
            e.p17_s1 = p17_s1
            e.p17_s2 = p17_s2
            e.p17_s3 = p17_s3
            e.p17_s4 = p17_s4
            e.p18_s1 = p18_s1
            e.p18_s2 = p18_s2
            e.p18_s3 = p18_s3
            e.p18_s4 = p18_s4
            e.compliance1_s1 = compliance1_s1
            e.compliance1_s2 = compliance1_s2
            e.compliance1_s3 = compliance1_s3
            e.compliance_1 = compliance_1
            e.compliance_2 = compliance_2

            e.overall_score = total_score
            e.fatal_count = no_of_fatals
            e.fatal = fatal
            e.added_by = added_by
            e.areas_improvement = areas_imp
            e.positives = positive
            e.comments = comments
            e.save()
            msg = 'Audit for ' + associate_name + ' is done Successfully!'
            messages.info(request, msg)
            return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def fameHouseSubmit(request):
    if request.method == 'POST':
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type

        associate_name = request.POST['empname']
        emp_id = request.POST['empid']

        ticket_no = request.POST['ticketnumber']
        ticket_type = request.POST['ticket_type']
        trans_date = request.POST['transdate']

        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        # Immediate fails:
        compliance_1 = int(request.POST['compliance_1'])
        compliance_2 = int(request.POST['compliance_2'])
        compliance_3 = int(request.POST['compliance_3'])
        compliance_4 = int(request.POST['compliance_4'])
        compliance_5 = int(request.POST['compliance_5'])
        compliance_6 = int(request.POST['compliance_6'])
        compliance_7 = int(request.POST['compliance_7'])
        compliance_8 = int(request.POST['compliance_8'])
        compliance_9 = int(request.POST['compliance_9'])
        compliance_10 = int(request.POST['compliance_10'])
        compliance_11 = int(request.POST['compliance_11'])

        compliance_total = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5 + compliance_6 + \
                           compliance_7 + compliance_8 + compliance_9 + compliance_10 + compliance_11

        sum_list = []

        def scoreCalc(pk):
            if pk == 'NA':
                sum_list.append(0)
                return pk
            else:
                sum_list.append(int(pk))
                return int(pk)

        # Customer Response
        cr_1 = scoreCalc(request.POST["cr_1"])

        # Opening
        opening_1 = scoreCalc(request.POST['opening_1'])
        opening_2 = scoreCalc(request.POST['opening_2'])

        # Composition
        comp_1 = scoreCalc(request.POST['comp_1'])
        comp_2 = scoreCalc(request.POST['comp_2'])

        # Macro
        macro_1 = scoreCalc(request.POST['macro_1'])
        macro_2 = scoreCalc(request.POST['macro_2'])

        # Closing
        closing_1 = scoreCalc(request.POST['closing_1'])
        closing_2 = scoreCalc(request.POST['closing_2'])

        # Customer Issue Resolution
        cir_1 = scoreCalc(request.POST['cir_1'])
        cir_2 = scoreCalc(request.POST['cir_2'])
        cir_3 = scoreCalc(request.POST['cir_3'])
        cir_4 = scoreCalc(request.POST['cir_4'])
        cir_5 = scoreCalc(request.POST['cir_5'])
        cir_6 = scoreCalc(request.POST['cir_6'])
        cir_7 = scoreCalc(request.POST['cir_7'])

        # Ettiqt
        et_1 = scoreCalc(request.POST['et_1'])
        et_2 = scoreCalc(request.POST['et_2'])
        et_3 = scoreCalc(request.POST['et_3'])
        et_4 = scoreCalc(request.POST['et_4'])
        et_5 = scoreCalc(request.POST['et_5'])

        # Documentation
        doc_1 = scoreCalc(request.POST['doc_1'])
        doc_2 = scoreCalc(request.POST['doc_2'])
        doc_3 = scoreCalc(request.POST['doc_3'])
        doc_4 = scoreCalc(request.POST['doc_4'])

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5, compliance_6,
                      compliance_7, compliance_8, compliance_9, compliance_10, compliance_11]

        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0 or compliance_6 == 0:
            overall_score = 0
            fatal = True
        elif compliance_7 == 0 or compliance_8 == 0 or compliance_9 == 0 or compliance_10 == 0 or compliance_11 == 0:
            overall_score = 0
            fatal = True
        else:
            if sum(sum_list) != 0:
                overall_score = (sum(sum_list) / len(sum_list)) * 100
            else:
                overall_score = 100
            fatal = False

        #################################################

        areas_improvement = request.POST['areaimprovement']
        positives = request.POST['positives']
        comments = request.POST['comments']

        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        try:
            FameHouse.objects.get(unique_id=unique_id)
            messages.info(request, "Please have patience! How ever the Audit has been Added :)")
            return redirect("/dashboard")
        except FameHouse.DoesNotExist:
            e = FameHouse()
            e.audit_id = audit_id
            e.unique_id = unique_id
            e.campaign = campaign_name
            e.campaign_type = campaign_type
            e.campaign_id = campaign_id
            e.associate_name = associate_name
            e.emp_id = emp_id
            e.ticket_type = ticket_type
            e.week = week
            e.trans_date = trans_date
            e.audit_date = audit_date
            e.ticket_no = ticket_no
            e.quality_analyst = quality_analyst
            e.team_lead = team_lead
            e.team_lead_id = team_lead_id
            e.manager = manager
            e.manager_id = manager_id
            e.am = am
            e.am_id = am_id

            e.compliance_1 = compliance_1
            e.compliance_2 = compliance_2
            e.compliance_3 = compliance_3
            e.compliance_4 = compliance_4
            e.compliance_5 = compliance_5
            e.compliance_6 = compliance_6
            e.compliance_7 = compliance_7
            e.compliance_8 = compliance_8
            e.compliance_9 = compliance_9
            e.compliance_10 = compliance_10
            e.compliance_11 = compliance_11
            e.compliance_total = compliance_total
            e.cr_1 = cr_1
            e.opening_1 = opening_1
            e.opening_2 = opening_2
            e.comp_1 = comp_1
            e.comp_2 = comp_2
            e.cir_1 = cir_1
            e.cir_2 = cir_2
            e.cir_3 = cir_3
            e.cir_4 = cir_4
            e.cir_5 = cir_5
            e.cir_6 = cir_6
            e.cir_7 = cir_7
            e.macro_1 = macro_1
            e.macro_2 = macro_2
            e.doc_1 = doc_1
            e.doc_2 = doc_2
            e.doc_3 = doc_3
            e.doc_4 = doc_4
            e.et_1 = et_1
            e.et_2 = et_2
            e.et_3 = et_3
            e.et_4 = et_4
            e.et_5 = et_5
            e.closing_1 = closing_1
            e.closing_2 = closing_2
            e.areas_improvement = areas_improvement
            e.positives = positives
            e.comments = comments

            e.added_by = added_by
            e.overall_score = overall_score
            e.fatal = fatal
            e.fatal_count = no_of_fatals
            e.audit_duration = duration
            e.save()
            msg = 'Audit for ' + associate_name + ' is done Successfully!'
            messages.info(request, msg)
            return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def ILMakiageSubmit(request):
    if request.method == 'POST':
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type

        associate_name = request.POST['empname']
        emp_id = request.POST['empid']

        zone = request.POST['zone']
        concept = request.POST['concept']
        customer_name = request.POST['customer']
        ticket_id = request.POST['ticketnumber']
        email_chat_date = request.POST['trans_date']
        query_type = request.POST['query_type']
        audit_date = request.POST['auditdate']
        quality_analyst = request.POST['qa']
        team_lead = request.POST['tl']
        team_lead_id = request.POST['tl_id']
        am = request.POST['am']
        am_id = request.POST['am_id']
        week = request.POST['week']
        manager = request.POST['manager']
        manager_id = request.POST['manager_id']

        lst = []
        lst_tot = []

        def addtoScore(score, tot):
            if score == 'NA':
                pass
            else:
                lst.append(int(score))
                lst_tot.append(tot)

        # Solution
        s_1 = request.POST['s_1']
        addtoScore(s_1, 10)

        s_2 = request.POST['s_2']
        addtoScore(s_2, 10)

        s_3 = request.POST['s_3']
        addtoScore(s_3, 10)

        s_4 = request.POST['s_4']
        addtoScore(s_4, 10)

        # Efficiency
        e_1 = request.POST['e_1']
        addtoScore(e_1, 10)

        e_2 = request.POST['e_2']
        addtoScore(e_2, 10)

        # Compliance
        compliance_1 = int(request.POST['compliance_1'])
        addtoScore(compliance_1, 10)

        compliance_2 = int(request.POST['compliance_2'])
        addtoScore(compliance_2, 10)

        compliance_3 = int(request.POST['compliance_3'])
        addtoScore(compliance_3, 10)

        fatal_list = [compliance_1, compliance_2, compliance_3]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)

        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0:
            overall_score = 0
            fatal = True
        else:
            overall_score = sum(lst) / sum(lst_tot)
            fatal = False

        areas_improvement = request.POST['areaimprovement']
        positives = request.POST['positives']
        comments = request.POST['comments']
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        try:
            ILMakiage.objects.get(unique_id=unique_id)
            messages.info(request, "Please have patience! How ever the Audit has been Added :)")
            return redirect("/dashboard")
        except ILMakiage.DoesNotExist:
            e = ILMakiage()
            e.audit_id = audit_id
            e.unique_id = unique_id
            e.campaign = campaign_name
            e.campaign_type = campaign_type
            e.campaign_id = campaign_id
            e.associate_name = associate_name
            e.emp_id = emp_id
            e.zone = zone
            e.concept = concept
            e.customer_name = customer_name
            e.ticket_id = ticket_id
            e.email_chat_date = email_chat_date
            e.query_type = query_type
            e.audit_date = audit_date
            e.quality_analyst = quality_analyst
            e.team_lead = team_lead
            e.team_lead_id = team_lead_id
            e.am = am
            e.am_id = am_id
            e.week = week
            e.manager = manager
            e.manager_id = manager_id
            e.s_1 = s_1
            e.s_2 = s_2
            e.s_3 = s_3
            e.s_4 = s_4
            e.e_1 = e_1
            e.e_2 = e_2
            e.compliance_1 = compliance_1
            e.compliance_2 = compliance_2
            e.compliance_3 = compliance_3
            e.areas_improvement = areas_improvement
            e.positives = positives
            e.comments = comments
            e.added_by = added_by
            e.overall_score = overall_score

            e.fatal_count = no_of_fatals
            e.fatal = fatal
            e.audit_duration = duration
            e.overall_score = overall_score
            e.save()
            msg = 'Audit for ' + associate_name + ' is done Successfully!'
            messages.info(request, msg)
            return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def WinopolySubmit(request):
    if request.method == 'POST':
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        disposition = request.POST["disposition"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        # Opening
        comp_1 = int(request.POST['comp_1'])
        op_2 = int(request.POST['op_2'])
        op_3 = int(request.POST['op_3'])
        op_4 = int(request.POST['op_4'])
        op_5 = int(request.POST['op_5'])
        op_total = op_2 + op_3 + op_4 + op_5

        # MATCHING PROCESS
        mp_1 = int(request.POST['mp_1'])
        mp_2 = int(request.POST['mp_2'])
        mp_3 = int(request.POST['mp_3'])
        mp_total = mp_1 + mp_2 + mp_3

        # CALL HANDLING PROCESS
        cp_1 = int(request.POST['cp_1'])
        cp_2 = int(request.POST['cp_2'])
        cp_3 = int(request.POST['cp_3'])
        cp_4 = int(request.POST['cp_4'])
        cp_5 = int(request.POST['cp_5'])
        cp_6 = int(request.POST['cp_6'])
        cp_total = cp_1 + cp_2 + cp_3 + cp_4 + cp_5 + cp_6

        #  Compliance
        comp_2 = int(request.POST['comp_2'])
        comp_3 = int(request.POST['comp_3'])
        comp_4 = int(request.POST['comp_4'])
        comp_5 = int(request.POST['comp_5'])

        # TP
        tp_1 = int(request.POST['tp_1'])
        tp_2 = int(request.POST['tp_2'])
        tp_3 = int(request.POST['tp_3'])
        comp_6 = int(request.POST['comp_6'])
        tp_total = tp_1 + tp_2 + tp_3

        evaluator_comment = request.POST['evaluator_comment']
        coaching_comments = request.POST['coaching_comments']

        compliance_total = comp_1 + comp_2 + comp_3 + comp_4 + comp_5 + comp_6

        fatal_list = [comp_1, comp_2, comp_3, comp_4, comp_5, comp_6]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)

        no_of_fatals = len(fatal_list_count)

        if comp_1 == 0 or comp_2 == 0 or comp_3 == 0 or comp_4 == 0 or comp_5 == 0 or comp_6 == 0:
            overall_score = 0
            fatal = True
        else:
            overall_score = op_total + mp_total + cp_total + tp_total
            fatal = False

        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        try:
            Winopoly.objects.get(unique_id=unique_id)
            messages.info(request, "Please have patience! How ever the Audit has been Added :)")
            return redirect("/dashboard")
        except Winopoly.DoesNotExist:
            e = Winopoly()
            e.audit_id = audit_id
            e.unique_id = unique_id
            e.audit_duration = duration
            e.overall_score = overall_score
            e.campaign = campaign_name
            e.campaign_type = campaign_type
            e.campaign_id = campaign_id
            e.associate_name = emp_name
            e.emp_id = emp_id
            e.zone = zone
            e.concept = concept
            e.customer_name = customer_name
            e.customer_contact = customer_contact
            e.disposition = disposition
            e.call_date = call_date
            e.call_duration = call_duration
            e.audit_date = audit_date
            e.quality_analyst = quality_analyst
            e.team_lead = team_lead
            e.manager = manager
            e.am = am
            e.team_lead_id = team_lead_id
            e.manager_id = manager_id
            e.am_id = am_id
            e.week = week

            e.comp_1 = comp_1
            e.op_2 = op_2
            e.op_3 = op_3
            e.op_4 = op_4
            e.op_5 = op_5
            e.op_total = op_total
            e.mp_1 = mp_1
            e.mp_2 = mp_2
            e.mp_3 = mp_3
            e.mp_total = mp_total
            e.cp_1 = cp_1
            e.cp_2 = cp_2
            e.cp_3 = cp_3
            e.cp_4 = cp_4
            e.cp_5 = cp_5
            e.cp_6 = cp_6
            e.cp_total = cp_total
            e.comp_2 = comp_2
            e.comp_3 = comp_3
            e.comp_4 = comp_4
            e.comp_5 = comp_5
            e.tp_1 = tp_1
            e.tp_2 = tp_2
            e.tp_3 = tp_3
            e.comp_6 = comp_6
            e.tp_total = tp_total
            e.evaluator_comment = evaluator_comment
            e.coaching_comment = coaching_comments

            e.added_by = added_by
            e.fatal_count = no_of_fatals
            e.fatal = fatal
            e.save()
            msg = 'Audit for ' + emp_name + ' is done Successfully!'
            messages.info(request, msg)
            return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def NerotelSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        zone = request.POST["zone"]
        concept = request.POST["concept"]
        customer_name = request.POST["customer"]
        customer_contact = request.POST["customercontact"]
        call_date = request.POST["calldate"]
        call_duration_hr = int(request.POST["durationh"]) * 3600
        call_duration_min = int(request.POST["durationm"]) * 60
        call_duration_sec = int(request.POST["durations"])
        call_duration = call_duration_hr + call_duration_min + call_duration_sec
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        # Engagement
        eng_1 = int(request.POST["e_1"])
        eng_2 = int(request.POST["e_2"])
        eng_3 = int(request.POST["e_3"])
        eng_4 = int(request.POST["e_4"])
        eng_5 = int(request.POST["e_5"])
        eng_6 = int(request.POST["e_6"])
        eng_7 = int(request.POST["e_7"])
        eng_8 = int(request.POST["e_8"])
        eng_9 = int(request.POST["e_9"])
        eng_score = eng_1 + eng_2 + eng_3 + eng_4 + eng_5 + eng_6 + eng_7 + eng_8 + eng_9

        # Resolution
        res_1 = int(request.POST["res_1"])
        res_2 = int(request.POST["res_2"])
        res_3 = int(request.POST["res_3"])
        res_4 = int(request.POST["res_4"])
        res_score = res_1 + res_2 + res_3 + res_4

        # Business needs
        compliance_1 = int(request.POST["busi_1"])
        compliance_2 = int(request.POST["busi_2"])
        compliance_3 = int(request.POST["busi_3"])
        compliance_4 = int(request.POST["busi_4"])
        compliance_score = compliance_1 + compliance_2 + compliance_3 + compliance_4

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = eng_score + res_score + compliance_score
            fatal = False
        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = Nerotel()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.eng_total = eng_score
        e.res_total = res_score
        e.compliance_total = compliance_score
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.zone = zone
        e.concept = concept
        e.customer_name = customer_name
        e.customer_contact = customer_contact
        e.call_date = call_date
        e.call_duration = call_duration
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week

        e.eng_1 = eng_1
        e.eng_2 = eng_2
        e.eng_3 = eng_3
        e.eng_4 = eng_4
        e.eng_5 = eng_5
        e.eng_6 = eng_6
        e.eng_7 = eng_7
        e.eng_8 = eng_8
        e.eng_9 = eng_9
        e.res_1 = res_1
        e.res_2 = res_2
        e.res_3 = res_3
        e.res_4 = res_4
        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.compliance_4 = compliance_4

        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)
        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def SpoiledChildSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        concept = request.POST["concept"]
        zone = request.POST["zone"]
        customer_name = request.POST["customer"]

        email_chat_date = request.POST["calldate"]
        audit_date = request.POST["auditdate"]
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]
        query_type = request.POST["query_type"]
        ticket_id = request.POST["ticketnumber"]

        solution_1 = int(request.POST["solution_1"])
        solution_2 = int(request.POST["solution_2"])
        solution_3 = int(request.POST["solution_3"])
        solution_4 = int(request.POST["solution_4"])
        solution_score = solution_1 + solution_2 + solution_3 + solution_4
        efficiency_1 = int(request.POST["efficiency_1"])
        efficiency_2 = int(request.POST["efficiency_2"])
        efficiency_score = efficiency_1 + efficiency_2
        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_score = compliance_1 + compliance_2 + compliance_3

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = solution_score + efficiency_score + compliance_score
            fatal = False

        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = SpoiledChild()
        e.audit_id = audit_id
        e.unique_id = unique_id
        e.audit_duration = duration
        e.overall_score = total_score
        e.campaign = campaign_name
        e.campaign_type = campaign_type
        e.campaign_id = campaign_id
        e.associate_name = emp_name
        e.emp_id = emp_id
        e.concept = concept
        e.email_chat_date = email_chat_date
        e.audit_date = audit_date
        e.quality_analyst = quality_analyst
        e.team_lead = team_lead
        e.manager = manager
        e.am = am
        e.team_lead_id = team_lead_id
        e.manager_id = manager_id
        e.am_id = am_id
        e.week = week
        e.areas_improvement = areas_imp
        e.positives = positive
        e.comments = comments
        e.fatal_count = no_of_fatals
        e.fatal = fatal
        e.added_by = added_by
        e.zone = zone
        e.customer_name = customer_name
        e.query_type = query_type
        e.ticket_id = ticket_id
        e.solution_1 = solution_1
        e.solution_2 = solution_2
        e.solution_3 = solution_3
        e.solution_4 = solution_4
        e.efficiency_1 = efficiency_1
        e.efficiency_2 = efficiency_2
        e.compliance_1 = compliance_1
        e.compliance_2 = compliance_2
        e.compliance_3 = compliance_3
        e.solution_score = solution_score
        e.efficiency_score = efficiency_score
        e.compliance_score = compliance_score
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def AmerisaveSubmit(request):
    if request.method == "POST":
        unique_id = request.POST["csrfmiddlewaretoken"]
        start = datetime.datetime.strptime(request.POST["start_time"], '%H:%M:%S.%f').time()
        end = datetime.datetime.now().time()
        duration = datetime.datetime.combine(date.today(), end) - datetime.datetime.combine(date.today(), start)
        duration = str(duration)
        campaign_id = request.POST["campaign_id"]
        campaign = Campaign.objects.get(id=campaign_id)
        campaign_name = campaign.name
        campaign_type = campaign.type
        emp_name = request.POST["empname"]
        emp_id = request.POST["empid"]
        type = request.POST["type"]
        lead_source = request.POST["lead_source"]
        customer_id = request.POST["customer_id"]
        transfer = request.POST["transfer"]

        call_date = request.POST["call_date"]
        audit_date = date.today()
        quality_analyst = request.POST["qa"]
        team_lead = request.POST["tl"]
        team_lead_id = request.POST["tl_id"]
        manager = request.POST["manager"]
        manager_id = request.POST["manager_id"]
        am = request.POST["am"]
        am_id = request.POST["am_id"]
        week = request.POST["week"]

        nce_1 = int(request.POST["nce_1"])
        nce_2 = request.POST["nce_2"]
        nce_3 = int(request.POST["nce_3"])
        nce_4 = int(request.POST["nce_4"])
        nce_score = nce_1 + nce_3 + nce_4

        compliance_1 = int(request.POST["compliance_1"])
        compliance_2 = int(request.POST["compliance_2"])
        compliance_3 = int(request.POST["compliance_3"])
        compliance_4 = int(request.POST["compliance_4"])
        compliance_5 = int(request.POST["compliance_5"])
        compliance_6 = int(request.POST["compliance_6"])
        compliance_score = compliance_1 + compliance_2 + compliance_3 + compliance_4 + compliance_5 + compliance_6

        areas_imp = request.POST["areaimprovement"]
        positive = request.POST["positives"]
        comments = request.POST["comments"]

        fatal_list = [compliance_1, compliance_2, compliance_3, compliance_4, compliance_5, compliance_6]
        fatal_list_count = []
        for i in fatal_list:
            if i == 0:
                fatal_list_count.append(i)
        no_of_fatals = len(fatal_list_count)

        if compliance_1 == 0 or compliance_2 == 0 or compliance_3 == 0 or compliance_4 == 0 or compliance_5 == 0 or compliance_6 == 0:
            total_score = 0
            fatal = True
        else:
            total_score = nce_score + compliance_score
            fatal = False

        added_by = request.user.profile.emp_id

        auditid = AuditIdTable.objects.first()
        audit_id = auditid.audit_id
        auditid.audit_id = int(auditid.audit_id) + 1
        auditid.save()

        e = Amerisave(
            unique_id=unique_id, audit_duration=duration, overall_score=total_score, campaign=campaign_name,
            campaign_type=campaign_type, campaign_id=campaign_id, associate_name=emp_name, emp_id=emp_id,
            call_date=call_date, audit_date=audit_date, quality_analyst=quality_analyst, team_lead=team_lead,
            manager=manager, am=am, team_lead_id=team_lead_id, manager_id=manager_id, am_id=am_id, week=week,
            areas_improvement=areas_imp, positives=positive, comments=comments, fatal_count=no_of_fatals,
            fatal=fatal, added_by=added_by, audit_id=audit_id,

            nce_1=nce_1, nce_2=nce_2, nce_3=nce_3, nce_4=nce_4,
            compliance_1=compliance_1, compliance_2=compliance_2, compliance_3=compliance_3,
            compliance_4=compliance_4, compliance_5=compliance_5, compliance_6=compliance_6,
            nce_score=nce_score, compliance_score=compliance_score, type=type, lead_source=lead_source,
            customer_id=customer_id, transfer=transfer,

        )
        e.save()

        msg = 'Audit for ' + emp_name + ' is done Successfully!'
        messages.info(request, msg)

        return redirect("/dashboard")
    else:
        messages.warning(request, 'Invalid request. You have been Logged out!')
        return redirect("/logout")


@login_required
def PasswordReset(request):
    emp = request.user.profile.emp_id
    if emp == '1234' or emp == '5670' or emp == '8413' or emp == '5533':
        if request.method == 'POST':
            emp_id = request.POST['empid']
            password = request.POST['password']
            confirm_pass = request.POST['confirmpass']
            if password == confirm_pass:
                e = User.objects.get(username=emp_id)
                e.password = make_password(password)
                e.save()
                messages.error(request, 'Password changed successfully!')
                return redirect('/password-reset')
            else:
                messages.error(request, 'Passwords does not match')
                return redirect('/password-reset')
        else:
            profiles = Profile.objects.all()
            data = {"profiles": profiles}
            return render(request, "password_reset.html", data)
    else:
        messages.error(request, 'Bad Request!')
        return redirect("/")


class TotalList(FlatMultipleModelAPIView):
    querylist = [
        {'queryset': Outbound.objects.all(),
         'serializer_class': OutboundSerializer},

        {'queryset': Inbound.objects.all(),
         'serializer_class': InboundSerializer},

        {'queryset': EmailChat.objects.all(),
         'serializer_class': EmailChatSerializer},

        {'queryset': DigitalSwissGold.objects.all(),
         'serializer_class': DigitalSwissGoldSerializer},

        {'queryset': FLA.objects.all(),
         'serializer_class': FLASerializer},

        {'queryset': BlazingHog.objects.all(),
         'serializer_class': BlazingHogSerializer},

        {'queryset': NoomPod.objects.all(),
         'serializer_class': NoomPodSerializer},

        {'queryset': NoomEva.objects.all(),
         'serializer_class': NoomEvaSerializer},

        {'queryset': AbHindalco.objects.all(),
         'serializer_class': AbHindalcoSerializer},

        {'queryset': FameHouse.objects.all(),
         'serializer_class': FameHouseSerializer},

        {'queryset': Practo.objects.all(),
         'serializer_class': PractoSerializer},

        {'queryset': ILMakiage.objects.all(),
         'serializer_class': ILMakiageSerializer},

        {'queryset': Winopoly.objects.all(),
         'serializer_class': WinopolySerializer},

        {'queryset': Nerotel.objects.all(),
         'serializer_class': NerotelSerializer},

        {'queryset': SpoiledChild.objects.all(),
         'serializer_class': SpoiledChildSerializer},

        {'queryset': Amerisave.objects.all(),
         'serializer_class': AmerisaveSerializer},
    ]
