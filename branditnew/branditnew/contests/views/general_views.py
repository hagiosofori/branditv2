from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader




def custom_admin(request):
    template = loader.get_template('contests/custom_admin.html')
    return HttpResponse(template.render())