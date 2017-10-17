from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'custom_admin'

urlpatterns = [
    url(r'^$', views.custom_admin_views.index, name="index"),

    url(r'^projects/(?P<project_id>[0-9]+)/', views.custom_admin_views.project_details, name='project_details'),

    url(r'^projects/(?p<project_id>[0-9]+)/', views.custom_admin_views.make_project_submission, name="make-project-submission"),

    
]