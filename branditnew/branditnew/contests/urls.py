from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views



app_name = 'contests'

urlpatterns = [
    url(r'^$', views.views.index, name='index'),
    url(r'^dashboard/', views.contest_views.dashboard, name='dashboard'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^create_contest/', views.contest_views.create_contest, name='create_contest'),
    url(r'^(?P<contest_id>[0-9]+)/entries/(?P<entry_id>[0-9]+)/make_winner/', views.make_winner, name="make_winner"),
    url(r'^(?P<contest_id>[0-9]+)/submit_entry/', views.submit_entry, name='submit_entry'),
    url(r'^(?P<contest_id>[0-9]+)/$', views.contest_details, name='contest_details'),
    url(r'^contest_list/$', views.contest_list, name="contest_list"),
    url(r'^(?P<contest_id>[0-9]+)/entries/(?P<entry_id>[0-9]+)/details/$',views.contest_views.entry_details, name="entry_details"),
    url(r'^(?P<contest_id>[0-9]+)/entries/(?P<entry_id>[0-9]+)/make_comment/$', views.contest_views.make_comment, name="make_comment"),
    url(r'^(?P<contest_id>[0-9]+)/edit/$', views.contest_views.create_contest, name="edit_contest"),

    url(r'^login/$', auth_views.login, {'template_name':'contests/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'contests/index.html'}, name='logout'),

    url(r'^test/$', views.test),
]