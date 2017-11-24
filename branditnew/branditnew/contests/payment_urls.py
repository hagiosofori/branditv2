from django.conf.urls import url

from . import views

app_name = 'payments'

urlpatterns = [
    url(r'^purchase_points/$', views.view_points, name="view_points"),
    
    url(r'^purchase_points/(?P<points_id>[0-9]+)$', views.purchase_points, name="purchase_points"),

    url(r'^purchase_points/verify_payment$', views.verify_points_purchase_payment, name="purchase_points_verify_payment"),

    url(r'^verify$', views.verify_payment, name="payment_verify"),

    url(r'^request_payment/(?P<achievement_id>[0-9]+)$',views.request_winning_entry_payment, name="request_payment" ),


]
