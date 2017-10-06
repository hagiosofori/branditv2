from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'projects'

urlpatterns = [
    url(r'^save_as_draft', views.projects_view.save_as_draft, name="save_as_draft"),

    url(r'^create', views.projects_view.create_project, name="create_project"),

    url(r'^project/(?P<project_id>[0-9]+)/edit', views.projects_view, name="project_edit"),
    
]