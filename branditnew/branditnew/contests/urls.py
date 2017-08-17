from django.conf.urls import url
from . import views

app_name = 'contests'

urlpatterns = [
    #eg: brandit.express/contests/ OR brandit.express/
    url(r'^$', views.index, name='contest-index'),

    url(r'^signup/', views.signup, name='signup'),
    
]