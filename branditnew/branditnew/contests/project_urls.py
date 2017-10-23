from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'projects'

urlpatterns = [
    url(r'^$', views.projects_view.index, name="myprojects"),

    url(r'^save_as_draft', views.projects_view.save_as_draft, name="save_as_draft"),

    url(r'^create', views.projects_view.create_project, name="create_project"),

    url(r'^(?P<project_id>[0-9]+)/edit', views.projects_view.edit_project, name="project_edit"),

    url(r'^(?P<project_id>[0-9]+)/details$', views.projects_view.project_details, name="project_details"),

    url(r'^(?P<project_id>[0-9]+)/submissions/(?P<submission_id>[0-9]+)/select', views.projects_view.select_design, name="select_design"),

    url(r'^(?P<project_id>[0-9]+)/submissions/(?P<submission_id>[0-9]+)/deselect', views.projects_view.deselect_design, name="deselect_design"),

    url(r'^(?P<project_id>[0-9]+)/submissions/(?P<submission_id>[0-9]+)/details', views.projects_view.submission_details, name="submission_details"),



]