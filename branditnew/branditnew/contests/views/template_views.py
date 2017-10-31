from django.shortcuts import render

from branditnew.contests.models.templates import Template, Template_Order




def templates_list(request):
    templates = Template.objects.all()
    context = {
        'templates': templates,
    }
    return render(request, "contests/templates.html", context)




def details(request, template_id):
    template = Template.objects.get(pk=template_id)

    context = {
        'template': template,
    }
    return render(request, "contests/template_details.html", context)




