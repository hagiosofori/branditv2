from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from branditnew.contests.models import categories, contest, entries, prices, projects




def index(request):
    template = loader.get_template('contests/custom_admin_base.html')
    new_projects_list = projects.Project.objects.filter(is_touched=False)
    old_projects_list = projects.Project.objects.filter(is_touched=True)
    contest_list = contest.Contest.objects.all()
    print(new_projects_list, contest_list)
    context = {
        'new_projects': new_projects_list,
        'contests': contest_list,
        'old_projects': old_projects_list,
        'num_new_projects': projects.get_num_new_projects,        
    }
    return HttpResponse(template.render(context))




def project_details(request, project_id):
    
    template = loader.get_template('contests/custom_admin_project_details.html')
    project_obj = projects.Project.objects.get(pk=project_id)
    project_obj.touch()
    context = {
        'project' : project_obj,
        'num_new_projects' : projects.get_num_new_projects(),
    }
    return HttpResponse(template.render(context))





def make_project_submission(request, project_id):
    