"""branditnew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from . import settings
from .contests import views

urlpatterns = [
    url(r'^$', views.home, name="home" ),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^create_project/', views.projects_view.create_project, name="create_project"),
    #eg: brandit.express/contests/
    url(r'^contests/', include('branditnew.contests.urls')),
    url(r'^projects/', include('branditnew.contests.project_urls')),

    # url(r'^payments/purchase_points/$', views.view_points, name="view_points"),
    
    # url(r'^payments/purchase_points/(?P<points_id>[0-9]+)', views.purchase_points, name="purchase_points"),

    # url(r'^payments/purchase_points/verify_payment', views.verify_points_purchase_payment, name="purchase_points_verify_payment"),

    # url(r'^payments/verify', views.verify_payment, name="payment_verify"),

    url(r'^payments/', include('branditnew.contests.payment_urls')),
    
    url(r'^print_orders/', include("branditnew.contests.print_order_urls")),

    #eg: brandit.express/admin
    url(r'^admin/', admin.site.urls),

    url(r'^custom_admin/', include('branditnew.contests.custom_admin_urls')),
    url(r'^templates/', include('branditnew.contests.template_urls')),
    url(r'oauth/', include('social_django.urls', namespace="social")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
