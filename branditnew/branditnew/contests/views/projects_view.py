from branditnew.contests.models import forms
from branditnew.contests.models.projects import *
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, reverse, get_object_or_404
from branditnew.contests.views.payment_views import process_invoice, verify_payment
from django.http import HttpResponse, HttpResponseRedirect
import requests, json



@login_required(login_url="login")
def create_project(request):
    form = forms.Create_Project_Form()
    category_prices = Category.objects.values()
    print(list(category_prices))

    if request.method == "POST":
        form = forms.Create_Project_Form(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            category_cost = Category.objects.get(name=form.cleaned_data.get('category')) 
            cost = category_cost.prize_lower_limit
            print(cost)
            project.cost = cost
            project.save()

            #hubtel payment goes here.
            data = process_invoice(request, project)
            return redirect(data['response_text'], data['token'])

    context = {
        'form':form,
        'category_prices': json.dumps(list(category_prices))
    }
    return render(request, "contests/create_project.html", context)