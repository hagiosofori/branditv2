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



def contests(request):
    if check_permissions(request) is not True:
        return redirect(reverse("contests:login"))

    template = loader.get_template('contests/custom_admin_contests.html')
    new_projects_list = projects.Project.objects.filter(is_touched=False)
    old_projects_list = projects.Project.objects.filter(is_touched=True)
    new_contest_list = contest.Contest.objects.filter(is_touched=False)
    old_contest_list = contest.Contest.objects.filter(is_touched=True)

    context = {
        'new_contests': new_contest_list,
        'old_contests': old_contest_list,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }

    return HttpResponse(template.render(context))



def contest_details(request, contest_id):
    contest_detail = Contest.objects.get(pk=contest_id)
    contest_detail.is_touched = True

    if contest_detail.payment_token: 
        verify_contest_payment(request, contest_id)
    
    contest_detail.refresh_from_db()

    context = {
        'contest': contest_detail,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,        
    }
    return render(request, 'contests/custom_admin_contest_details.html', context)





def verify_contest(request, contest_id):
    contest_obj = Contest.objects.get(pk=contest_id)
    contest_obj.is_verified = True
    contest_obj.is_touched = True
    contest_obj.save()
    messages.add_message(request, messages.SUCCESS, "Successfully verified contest", extra_tags='alert alert-success')





def verify_contest_payment(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    contest_token = contest.payment_token
    transaction = Transaction.objects.get(token=contest_token)
    is_paid = verify_payment(request, transaction)

    if is_paid:
        contest.is_paid_for = True
        contest.save()
        messages.add_message(request, message.SUCCESS, "Contest is paid for", extra_tags="alert alert-success")
    else:
        messages.add_message(request, message.ERROR, 'Contest is not paid for', extra_tags="alert alert-danger")
    
    return redirect(reverse("custom_admin:contests"))




