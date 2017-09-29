from branditnew.contests.models import forms
from branditnew.contests.models.projects import *
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, reverse, get_object_or_404
from branditnew.contests.views.payment_views import make_payment, verify_payment

import requests



@login_required(login_url="login")
def create_project(request):
    form = forms.Create_Project_Form()
    

    if request.method == "POST":
        form = forms.Create_Project_Form(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            category_cost = Category.objects.get(name=form.cleaned_data.get('category')) 
            cost = category_cost.prize_lower_limit
            print(cost)
            project.save()

            #hubtel payment goes here.
            make_payment(request, project)
    

    context = {
        'form':form,
    }
    return render(request, "contests/create_project.html", context)