from branditnew.contests.models import forms
from branditnew.contests.models.projects import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, reverse, get_object_or_404
from branditnew.contests.views.payment_views import process_invoice, verify_payment
from django.http import HttpResponse, HttpResponseRedirect
import requests, json, pprint



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
        print(request.POST.keys())
        print(request.FILES.keys())
        # title = request.POST["title"]
        # category = request.POST['category']
        # desc = request.POST['description']
        # files = request.POST.FILES['files']
        # end_date = request.POST['end_date']

        # draft = Project.objects.create(title=title, category=category, description=desc, files=files, end_date=end_date)
        # draft.save()

        return HttpResponse('success')
    #     title = request.POST['title']

    #     try:
    #         draft = Project.objects.create(title=title)
    #         draft.save()
    #     except:
    #         pass
    # else:
    #     # Somehow to retrieve data from db here OR is it going into *load_draft* function with its own jQuery? adding adding data into fields
    #     nothing = "nothing"
