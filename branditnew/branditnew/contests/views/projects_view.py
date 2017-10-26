import requests, json
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages

from branditnew.contests.models import forms
from branditnew.contests.models.projects import *
from branditnew.contests.views.payment_views import process_invoice, verify_payment



@login_required
def index(request):
    template = loader.get_template('contests/myprojects.html')
    projects = Project.objects.filter(client=request.user)

    context = {
        'projects': projects,
    }
    
    return HttpResponse(template.render(context))





@login_required(login_url="login")
def create_project(request):
    form = forms.Create_Project_Form()
    category_prices = Category.objects.values()

    if request.method == "POST":
        form = forms.Create_Project_Form(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            category_cost = Category.objects.get(name=form.cleaned_data.get('category')) 
            cost = category_cost.prize_lower_limit
            project.cost = cost
            project.is_draft = False
            project.save()

            #hubtel payment goes here.
            data = process_invoice(request, project)
            return redirect(data['response_text'], data['token'])

    context = {
        'form':form,
        'category_prices': json.dumps(list(category_prices))
    }
    return render(request, "contests/create_project.html", context)




@csrf_exempt
def save_as_draft(request):
    if request.method == 'POST':
        client = request.user
        if request.POST['title'] is not '':
            title = request.POST["title"]
        else:
            title = 'draft'
        
        #fetching category instance using id from POST array. if no category has been set, use the 'draft' category, else django won't let you save.
        category_id = request.POST['category']
        if category_id is not '':
            category = Category.objects.filter(pk=category_id)
        else:
            category = Category.objects.get(name="draft")

        desc = request.POST['description']
        #files = request.POST.FILES['files'] yet to figure out how to handle the files upload part.
        end_date = request.POST['end_date']
        draft = Project.objects.create(client=client, title=title, category=category, description=desc, end_date=end_date)
        
        return HttpResponse('success')


def edit_project(request):
    if request.method == 'POST':
        return
    
    return 



def project_details(request, project_id):
    project = Project.objects.get(pk=project_id)
    project_submissions = Project_Submission.objects.filter(project=project)
    try:
        chosen_design = Project_Submission.objects.get(is_approved=True)
    except Project_Submission.DoesNotExist:
        chosen_design = None

    context = {
        'project':project,
        'project_submissions':project_submissions,
        'chosen_design':chosen_design,
    }
    return render(request, "contests/project_details.html", context)





def select_design(request, project_id, submission_id):
    submission = Project_Submission.objects.get(pk=submission_id)
    #make sure that before selecting this design no designs have been previously selected
    project = Project.objects.get(pk=project_id)
    current_selected = Project_Submission.objects.filter(is_approved=True, project=project)
    current_selected.is_approved = True
    
    submission = Project_Submission.objects.get(pk=submission_id)
    submission.is_approved = True
    submission.save()
    submissions_set = Project_Submission.objects.filter(project=project)
    messages.add_message(request, messages.SUCCESS, "Successfully selected design as winner", extra_tags='alert alert-success')
    context = {
        'project':project,
        'project_submissions':submissions_set,
        'chosen_design':submission,
    }
    return redirect(reverse('projects:project_details', args=(project_id)))





def deselect_design(request, project_id, submission_id):
    submission = Project_Submission.objects.get(pk=submission_id)
    
    project = Project.objects.get(pk=project_id)
    submission_set = Project_Submission.objects.filter(project=project)

    submission.is_approved = False
    submission.save()
    messages.add_message(request, messages.SUCCESS, "Successfully deselected design", extra_tags='alert alert-success')

    context = {
        'project':project,
        'project_submission':submission_set,
    }
    return redirect(reverse('projects:project_details', args=(project_id)))




def submission_details(request, project_id, submission_id):
    if request.method == 'POST':
        make_comment(request, submission_id, project_id)
    
    project = Project.objects.get(pk=project_id)
    submission = Project_Submission.objects.get(pk=submission_id)
    comments = Project_Submission_Comment.objects.filter(project_submission=submission)
    
    form = forms.Project_Submission_Comment_Form()
    context = {
        'comments': comments,
        'submission': submission,
        'project': project,
        'form': form,
    }
    return render(request, 'contests/project_submission_details.html', context)





def make_comment(request, submission_id, project_id):
    print("successfully entered make_comment view")
    form = forms.Project_Submission_Comment_Form(request.POST)

    if form.is_valid():
        submission = Project_Submission.objects.get(pk=submission_id)

        comment = form.save(commit=False)
        comment.owner = request.user
        comment.project_submission = submission
        comment.save()
        messages.add_message(request, messages.SUCCESS, "Comment successfully added", extra_tags='alert alert-success')
    else:
        messages.add_message(request, messages.error, 'Unable to save comment. Please try again after a while', extra_tags="alert alert-danger")

    return redirect(reverse("projects:submission_details", args=(project_id, submission_id)))





