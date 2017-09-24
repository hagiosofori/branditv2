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
from branditnew.contests.models.entries import Entry
import requests

# Create your views here.

def test(request):
    template = loader.get_template('contests/home.html')
    return(HttpResponse(template.render()))



def home(request):
    return redirect(reverse('contests:index'))



def index(request):
    top_contests = Contest.objects.filter(is_top="True", is_sealed="False", is_verified="True")
    completed_contests = Contest.objects.filter(is_closed=True)[:3]
    template = loader.get_template('contests/home.html')
    context = {
        'top_contests': top_contests,
        'closed_contests': completed_contests,
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
    return render(request, 'contests/login.html', context)



@login_required(login_url="contests:login")
def dashboard(request):
    template = loader.get_template('contests/dashboard.html')
    contests = Contest.objects.filter(client=request.user)
    context = {
        'contests': contests,
    }
    return render(request, 'contests/dashboard.html', context)



def create_contest(request):
    form = forms.CreateContestForm(initial={'would_like_to_print':True,})
    
    if request.method == 'POST':
        form = forms.CreateContestForm(request.POST, request.FILES)
        
        if form.is_valid():
            contest = form.save(commit=False)
            contest.client = request.user
            contest.cost = 300 #create a way to get this from the form
            """
            #hubtel payment code.
            merchant_account_name = ""
            hubtel_payment_url = "api.hubtel.com/"+merchant_account_name+"v1/"+merchant_account_name+"onlinecheckout/invoice/create"
            hubtel_post_data = {
                "invoice":{
                    "total_amount": contest.cost,
                    "description": contest.title,

                },
                "store":{
                    "name": "Brandit",
                    "tagline" "Africa’s largest online graphic design marketplace ",
                    "phone": "+233 549 2424 05",
                    "logo_url": "https://brandit.express/images/logo.png"
                    "website_url": "https://brandit.express/dashboard.php",
                }
                "actions":{
                    "cancel_url": "http://brandit.express/create_contest",
                    "return_url": "http://brandit.express/dashboard"
                }
            }

            response = requests.post(hubtel_payment_url, json=hubtel_post_data)
            """
            #check if the payment has been made, and update db accordingly before saving.
            contest.save()
            return redirect(reverse('contests:dashboard'))
    
    return render(request, "contests/create_contest.html", {'form': form})



def submit_entry(request, contest_id):
    form = forms.ContestEntryForm(initial={'contest': contest_id, 'brandlancer': request.user.id})

    if request.method == "POST":
        form = forms.ContestEntryForm(request.POST, request.FILES)

        if form.is_valid():
            entry = form.save(commit=False)
            current_contest = Contest.objects.get(pk=contest_id)
            entry.contest = current_contest
            entry.brandlancer = request.user
            entry.save()
            return redirect(reverse("contests:dashboard"))

    return render(request, "contests/submit_contest_entry.html", {'form': form})



def contest_details(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    winning_entry = Entry.objects.get(is_winner=True)
    context = {
        'contest': contest,
        'winning_entry': winning_entry,
    }
    return render(request, 'contests/contest_details.html', context)


def contest_list(request):
    contests_list = Contest.objects.all()
    template = loader.get_template('contests/contest_list.html')
    context = {
        'contests_list': contests_list,
    }
    return HttpResponse(template.render(context))



def make_winner(request, contest_id, entry_id):
    contest = Contest.objects.get(id=contest_id)
    entry = Entry.objects.get(pk=entry_id, contest__id=contest_id)
    current_winners = Entry.objects.get(is_winner=True, contest__id=contest_id)
    current_winners.is_winner = False

    entry.is_winner = True
    contest.is_closed = True
    contest.save()
    entry.save()
    current_winners.save()
    return redirect(reverse('contests:contest_details', args=(contest_id)))

