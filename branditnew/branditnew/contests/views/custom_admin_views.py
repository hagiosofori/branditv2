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
from branditnew.contests.models import touch
from branditnew.contests.models.transactions import Transaction

def check_permissions(request):
    if request.user.is_superuser is False:
        messages.add_message(request, messages.ERROR, "You do not have permission to access that section",extra_tags="alert-danger")
        return False

    return True


    


def index(request):
    if check_permissions(request) is not True:
        return redirect(reverse("contests:login"))

    template = loader.get_template('contests/custom_admin_base.html')
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




#PROJECTS FUNCTIONS


def project_details(request, project_id):
    if check_permissions(request) is False:
        return redirect(reverse("contests:login"))

    template = loader.get_template('contests/custom_admin_project_details.html')
    project_obj = projects.Project.objects.get(pk=project_id)
    project_obj.touch()

    context = {
        'project' : project_obj,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }

    return HttpResponse(template.render(context))





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


## CONTEST FUNCTIONS


def contests(request):
    if check_permissions(request) is not True:
        return redirect(reverse("contests:login"))

    template = loader.get_template('contests/custom_admin_contests.html')
    new_projects_list = projects.Project.objects.filter(is_touched=False)
    old_projects_list = projects.Project.objects.filter(is_touched=True)
    contest_list = contest.Contest.objects.all()

    context = {
        'contests': contest_list,

        'num_new_projects': projects.get_num_new_projects,
        'num_new_contest_entry_comments': entries.get_num_new_contest_entry_comments,
        'num_new_contests': contest.get_num_new_contests,
        'num_new_print_orders': print_orders.get_num_new_print_orders,
    }

    return HttpResponse(template.render(context))





def verify_contest(request, contest_id):
    contest_obj = Contest.objects.get(pk=contest_id)
    contest_obj.is_verified = True
    contest_obj.is_touched = True
    contest_obj.save()
    messages.add_message(request, messages.SUCCESS, "Successfully verified contest", extra_tags='alert alert-success')

    return redirect(reverse( "custom_admin:contests"))





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

    
#PRINT ORDERS FUNCTIONALITY


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

