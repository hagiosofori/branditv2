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
from branditnew.contests.custom_admin_views.custom_admin_general_views import check_permissions




def make_project_submission(request, project_id):
    if check_permissions(request) is False:
        return redirect(reverse("contests:login"))

    form = Make_Project_Submission_Form()

    if request.method == "POST":
        form = Make_Project_Submission_Form(request.POST, request.FILES)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.project = projects.Project.objects.get(pk=project_id)
            submission.save()
            print(submission)

            submission.project.add_submission()
            submission.project.touch() 
            
            messages.add_message(request, messages.SUCCESS, "Project submission successfully made", extra_tags="alert-success")

            return redirect(reverse("custom_admin:project_details", args=[project_id]))       

    project = projects.Project.objects.get(pk=project_id)

    context = {
        'project': project,
        'form': form,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }

    return render(request, "contests/custom_admin_make_project_submission.html", context)

