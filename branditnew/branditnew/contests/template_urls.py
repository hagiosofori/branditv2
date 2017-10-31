from django.conf.urls import url
from . import views



app_name = 'templates'

urlpatterns = [
    url(r'^$', views.template_views.templates_list, name='templates_list'),

    url(r'^(?P<template_id>[0-9]+)/details', views.template_views.details, name="template_details"),
]