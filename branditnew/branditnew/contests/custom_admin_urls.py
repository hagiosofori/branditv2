from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'custom_admin'

urlpatterns = [
    url(r'^$', views.custom_admin_views.index, name="index"),

    url(r'^projects/(?P<project_id>[0-9]+)/make_project_submission$', views.custom_admin_views.make_project_submission, name="make_project_submission"),

    url(r'^projects/(?P<project_id>[0-9]+)/$', views.custom_admin_views.project_details, name='project_details'),

    url(r'^contests/$', views.custom_admin_views.contests, name="contests"),    

    url(r'^contests/(?P<contest_id>[0-9]+)/verify$', views.custom_admin_views.verify_contest, name="verify_contest"),

    url(r'^contests/entries/comments/$', views.custom_admin_views.contest_entries_comments, name="contest_entries_comments"),

    url(r'^contests/entries/comments/(?P<comment_id>[0-9]+)/verify$', views.custom_admin_views.verify_entry_comment, name="verify_entry_comment"),
    
]