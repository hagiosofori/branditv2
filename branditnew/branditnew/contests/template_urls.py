from django.conf.urls import url
from . import views



app_name = 'templates'

urlpatterns = [
    url(r'^$', views.template_views.templates_list, name='templates_list'),


]