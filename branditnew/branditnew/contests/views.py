from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    html = "<h1>This is the index page</h1><br>"
    html += "<a href='% url '\signup\'>Click here to register on brandit</a>"
    return HttpResponse(html)