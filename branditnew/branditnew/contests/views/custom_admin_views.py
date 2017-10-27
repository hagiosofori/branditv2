from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import reverse, redirect, render
from django.contrib import messages

from branditnew.contests.models import categories, contest, entries, prices, projects
from branditnew.contests.models.forms import Make_Project_Submission_Form



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

    }

    return HttpResponse(template.render(context))




def project_details(request, project_id):
    if check_permissions(request) is False:
        return redirect(reverse("contests:login"))

    template = loader.get_template('contests/custom_admin_project_details.html')
    project_obj = projects.Project.objects.get(pk=project_id)
    project_obj.touch()

    context = {
        'project' : project_obj,
        'num_new_projects' : projects.get_num_new_projects(),
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
        'num_new_projects': projects.get_num_new_projects,
        'form': form,
    }

    return render(request, "contests/custom_admin_make_project_submission.html", context)





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

    }

    return HttpResponse(template.render(context))