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




def print_orders_list(request):
    new_print_orders = Print_Order.objects.filter(is_touched=False)
    old_print_orders = Print_Order.objects.filter(is_touched=True)

    context = {
        'new_print_orders': new_print_orders,
        'old_print_orders': old_print_orders,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }
    return render(request, "contests/custom_admin_print_orders.html", context)




def print_order_details(request, print_order_id):
    print_order = Print_Order.objects.get(pk=print_order_id)
    print_order.touch()

    if print_order.payment_token:
        verify_print_order_payment(request, print_order_id)
    

    context = {
        'print_order': print_order,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }

    return render(request, 'contests/custom_admin_print_order_details.html', context)



def verify_print_order_payment(request, print_order_id):
    print("done with verifying payment")
    print_order = Print_Order.objects.get(pk=print_order_id)
    transaction = Transaction.objects.get(token=print_order.payment_token)
    is_paid = verify_payment(request, transaction)

    if is_paid:
        print_order.is_paid = True
        print_order.save()
        messages.add_message(request, messages.SUCCESS, "Print order is paid for", extra_tags="alert alert-success")
    else:
        messages.add_message(request, messages.ERROR, 'Print order is not paid for', extra_tags="alert alert-danger")

