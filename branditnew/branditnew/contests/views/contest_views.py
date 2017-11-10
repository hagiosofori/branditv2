import requests, json
from datetime import datetime, timedelta

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

from branditnew.contests.models import forms
from branditnew.contests.models.contest import Contest
from branditnew.contests.models.entries import Entry, Entry_Comment
from branditnew.contests.models.prices import Price
from branditnew.contests.models.categories import Category
from branditnew.contests.models.projects import *
from branditnew.contests.views.payment_views import process_invoice


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
            return render(request, 'contests/dashboard.html')
        
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
    projects = Project.objects.filter(client=request.user)
    accomplishments = Entry.objects.filter(brandlancer=request.user, is_winner=True)
    context = {
        'contests': contests,
        'projects': projects,
        'accomplishments': accomplishments,
    }
    return HttpResponse(template.render(context))




# by default render the form for creating a contest.
# if the method is a post, store the values, save the contest object in the db, store the key of the obj, and redirect to the verify contest page.
    # if it's a post method, and there's already a key in the session, use that key. else, create a new contest object.

# also the edit function. in that case, the contest_id will be set, and the form will be populated with the details of the specified contest.
@login_required(login_url="contests:login")
def create_contest(request, contest_id=None):
    contest = None
    print(contest_id)
    if contest_id:
        contest = get_object_or_404(Contest, pk=contest_id)
    
    form = forms.CreateContestForm(instance=contest)
    category_prices = Category.objects.values()
    
    if request.method == 'POST':
        form = forms.CreateContestForm(request.POST, request.FILES, instance=contest)
        print(form)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.client = request.user
            category_cost = Category.objects.get(name=form.cleaned_data.get('category')) 
            cost = category_cost.prize_lower_limit
            contest.cost = form.cleaned_data.get('prize')
            contest.is_draft = False

            contest.save()

            return redirect(reverse('contests:verify_contest', args=[contest.id]))

    prices = Price.objects.values()
    
    context = {
        'form': form,
        'prices': json.dumps(list(prices), cls=DjangoJSONEncoder),
        'category_prices': json.dumps(list(category_prices)),
    }
    
    return render(request, "contests/create_contest.html", context)






def verify_contest(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    print(contest.cost)
    if request.method == "POST":
        messages.add_message(request, messages.SUCCESS, "Successfully created contest", extra_tags='alert alert-success')

        data = process_invoice(request, contest)
        print(data)

        return redirect(data['response_text'], data['token'])

    context = {
        'contest': contest,
    }
    return render(request, 'contests/verify_contest.html', context)








@login_required
def save_contest_as_draft(request):
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
        prize = request.POST['prize']
        is_top = request.POST['is_top']
        is_hidden = request.POST['is_hidden']
        is_nda = request.POST['is_nda']
        is_sealed = request.POST['is_sealed']
        preferred_styles = request.POST['preferred_style']
        preferred_colors = request.POST['preferred_colors']
        target_audience = request.POST['target_audience']
        design_details = request.POST['design_details']
        would_like_to_print = request.POST['would_like_to_print']
        
        #logo = 
        #sketch = 
        #files =

        draft = Contest.objects.create(client=client, title=title, category=category, description=desc, end_date=end_date, prize=prize, is_top=is_top, is_hidden=is_hidden, is_nda=is_nda, is_sealed=is_sealed, preferred_styles=preferred_styles, preferred_colors=preferred_colors, target_audience=target_audience, design_details=design_details, would_like_to_print=would_like_to_print)

        return HttpResponse('success')





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

    prices = Price.objects.values()
    print(prices)
    
    context = {
        'form': form,
        'prices': prices,
    }
    return render(request, "contests/submit_contest_entry.html", context)





def contest_details(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    try:
        winning_entry = Entry.objects.get(is_winner=True, contest=contest)
    except Entry.DoesNotExist:
        winning_entry = None
    
    context = {
        'contest': contest,
        'winning_entry': winning_entry,
    }
    print("accidentally coming here")
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





#entry details
def entry_details(request, contest_id, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    contest = Contest.objects.get(pk=contest_id)
    comments = Entry_Comment.objects.filter(contest_entry=entry, is_verified=True)
    form = forms.Entry_Comment_Form();
    context = {
        'entry': entry,
        'contest': contest,
        'comments':comments,
        'form':form,
    }
    print("inside contest entry details view")
    return render(request, 'contests/contest_entry_details.html', context)





def make_comment(request, contest_id, entry_id):
    form = forms.Entry_Comment_Form(request.POST)

    if form.is_valid():
        entry = Entry.objects.get(pk=entry_id)
        client = entry.contest.client
        comment = form.save(commit=False)
        comment.owner = request.user
        comment.contest_entry = entry

        #the contest owner's comments are automatically verified. Brandlancers would have to be verified by the admin. is_verified field of entry_comments table defaults to False if no value is provided.
        if comment.owner == client:
            comment.is_verified = True
            comment.is_touched = True
        
        comment.save()
        messages.add_message(request, messages.SUCCESS, "Comment successfully saved", extra_tags='alert alert-success')
    else:
        messages.add_message(request, messages.error, 'Unable to save comment. Please try again after a while', extra_tags="alert alert-danger")

    return redirect(reverse("contests:entry_details", args=(contest_id, entry_id)))