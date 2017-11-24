from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import reverse, redirect, render
from django.contrib import messages

from branditnew.contests.models import categories, contest, entries, prices, projects
from branditnew.contests.models.contest import Contest
from branditnew.contests.models.forms import Make_Project_Submission_Form
from branditnew.contests.models.print_orders import Item, Print_Order
from branditnew.contests.models import print_orders
from branditnew.contests.models.transactions import Transaction
from branditnew.contests.views import verify_payment
from branditnew.contests.views.custom_admin_views.custom_admin_general_views import check_permissions


def projects_list(request):
    if check_permissions(request) is not True:
        return redirect(reverse("contests:login"))

    template = loader.get_template('contests/custom_admin_projects.html')
    new_projects_list = projects.Project.objects.filter(is_touched=False)
    old_projects_list = projects.Project.objects.filter(is_touched=True)
    contest_list = contest.Contest.objects.all()

    context = {
        'new_projects': new_projects_list,
        'contests': contest_list,
        'old_projects': old_projects_list,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,

    }

    return HttpResponse(template.render(context))




def verify_project_payment(request, project_id):
    project = Project.objects.get(pk=project_id)
    project_token = project.payment_token
    transaction = Transaction.objects.get(token=project_token)
    is_paid = verify_payment(request, transaction)

    if is_paid:
        project.is_paid = True
        project.save()
        messages.add_mesesage(request, messages.SUCCESS, 'Contest is paid for', extra_tags="alert alert-success")
    else:
        messages.add_message(request, messages.ERROR, "Contest is not paid for", extra_tags="alert alert-danger")
    



def project_details(request, project_id):
    if check_permissions(request) is False:
        return redirect(reverse("contests:login"))

    template = loader.get_template('contests/custom_admin_project_details.html')
    project_obj = projects.Project.objects.get(pk=project_id)
    project_obj.touch()

    if project_obj.payment_token:
        verify_project_payment(request, project_id)
    
    project_obj.refresh_from_db()
    submissions = projects.Project_Submission.objects.filter(project=project_obj)
    print(submissions)
    context = {
        'project' : project_obj,
        'submissions': submissions,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }

    return HttpResponse(template.render(context))





