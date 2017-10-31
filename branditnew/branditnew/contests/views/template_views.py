from django.shortcuts import render

from branditnew.contests.models.templates import Template, Template_Order




def templates_list(request):
    templates = Template.objects.all()
    context = {
        'templates': templates,
    }
    return render(request, "contests/templates.html", context)