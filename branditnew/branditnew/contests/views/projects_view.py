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
    category_prices = Category.objects.all()
    print(category_prices[0])
    if request.method == "POST":
        form = forms.Create_Project_Form(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.cost = 300 #create way to extract this from template
            project.save()

            #hubtel payment goes here.
            make_payment(request, project)
    

    context = {
        'form':form,
        'category_prices': category_prices,
    }
    return render(request, "contests/create_project.html", context)