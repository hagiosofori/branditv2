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

    context = {
        'print_order': print_order,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }

    return render(request, 'contests/custom_admin_print_order_details.html', context)


#TRANSACTIONS
def transactions_list(request):
    transactions = Transaction.objects.all()
    context = {
        'transactions': transactions,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }

    return render(request, 'contests/custom_admin_transactions.html', context)

