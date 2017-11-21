from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import reverse, redirect, render

from branditnew.contests.models import categories, contest, entries, prices, projects
from branditnew.contests.models.contest import Contest
from branditnew.contests.models.forms import Make_Project_Submission_Form
from branditnew.contests.models.print_orders import Item, Print_Order
from branditnew.contests.models import print_orders
from branditnew.contests.models.transactions import Transaction
from branditnew.contests.views import verify_payment



def contest_entries_comments(request):
    if check_permissions(request) is not True:
        return redirect(reverse("contests:login"))
    
    comments = entries.Entry_Comment.objects.all()

    context = {
        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,

        'comments': comments
    }
    
    return render(request, "contests/custom_admin_contest_entries_comments.html", context)





def verify_entry_comment(request, comment_id):
    comment = entries.Entry_Comment.objects.get(pk=comment_id)
    comment.is_touched = True
    comment.is_verified = True
    comment.save()
    messages.add_message(request, messages.SUCCESS, "Successfully verified comment", extra_tags='alert alert-success')

    return redirect(reverse('custom_admin:contest_entries_comments'))

