from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "contests/index.html")



def signup(request):
    return ''
