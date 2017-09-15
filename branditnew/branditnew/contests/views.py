from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.template import loader
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from branditnew.contests.models import forms
from branditnew.contests.models.contest import Contest

# Create your views here.

def test(request):
    template = loader.get_template('contests/includes/side_nav.html')
    return(HttpResponse(template.render()))

def index(request):
    contests_list = Contest.objects.all()
    template = loader.get_template('contests/index.html')
    context = {
        'contests_list': contests_list,
    }
    return HttpResponse(template.render(context))



def signup(request):
    form = forms.SignUpForm() 
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.user_name = user.username
            raw_password = form.cleaned_data.get('password1')
            user.save()
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            template = loader.get_template('contests/dashboard.html')
            context = {}
            return render(request, 'contests/dashboard.html', context)
        else:
            print("form is not valid")
            print(form.error_messages)

    print("didn't submit the data")
    return render(request, "contests/signup.html", {'form': form})



def signin(request): 
    form = forms.SignInForm()

    if request.method == "POST":
        form = forms.SignInForm(request.POST)

        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            pword = form.cleaned_data.get('password')
            user = authenticate(username=user_name, password=pword)
            if user is not None:
                login(request, user)
                return redirect(reverse('contests:dashboard'))

    context = {
        'form': form
    }
    print(form.errors_messages)
    return render(request, 'contests/login.html', context)



@login_required(login_url="contests:login")
def dashboard(request):
    template = loader.get_template('contests/dashboard.html')
    return render(request, 'contests/dashboard.html')



def create_contest(request):
    form = forms.CreateContestForm(initial={'would_like_to_print':True,})
    
    if request.method == 'POST':
        form = forms.CreateContestForm(request.POST, request.FILES)
        
        if form.is_valid():
            print('form is valid')
            contest = form.save(commit=False)
            contest.client = request.user
            contest.cost = 300
            print(contest.end_date)
            contest.save()
            print(contest)
            return redirect(reverse('contests:dashboard'))

    
    return render(request, "contests/create_contest.html", {'form': form})



def submit_entry(request, contest_id):
    form = forms.ContestEntryForm(initial={'contest': contest_id, 'brandlancer': request.user.id})

    if request.method == "POST":
        form = forms.ContestEntryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, "contests/dashboard.html")

    return render(request, "contests/submit_contest_entry.html", {'form': form})



def contest_details(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    return render(request, 'contests/contest_details.html', {'contest': contest})
