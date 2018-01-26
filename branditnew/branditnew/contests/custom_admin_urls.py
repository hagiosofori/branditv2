from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
from .views.custom_admin_views import custom_admin_general_views, custom_admin_contest_views, custom_admin_general_views, custom_admin_print_order_views, custom_admin_project_views, custom_admin_project_submission_views, custom_admin_contest_entry_views, custom_admin_transaction_views, custom_admin_payment_request_views



app_name = 'custom_admin'

urlpatterns = [
    url(r'^$', custom_admin_project_views.projects_list, name="index"),

    url(r'^projects$', custom_admin_project_views.projects_list, name="index"),

    url(r'^projects/(?P<project_id>[0-9]+)/make_project_submission$', custom_admin_project_submission_views.make_project_submission, name="make_project_submission"),

    url(r'^projects/(?P<project_id>[0-9]+)/$', custom_admin_project_views.project_details, name='project_details'),

    url(r'^contests/$', custom_admin_contest_views.contests, name="contests"),    

    url(r'^contests/(?P<contest_id>[0-9]+)/details$', custom_admin_contest_views.contest_details, name="contest_details"),

    url(r'^contests/(?P<contest_id>[0-9]+)/verify$', custom_admin_contest_views.verify_contest, name="verify_contest"),

    url(r'^contests/entries/comments/$', custom_admin_contest_entry_views.contest_entries_comments, name="contest_entries_comments"),

    url(r'^contests/entries/comments/(?P<comment_id>[0-9]+)/verify$', custom_admin_contest_entry_views.verify_entry_comment, name="verify_entry_comment"),

    url(r'^print_orders$', custom_admin_print_order_views.print_orders_list, name="print_orders"),

    url(r'^print_orders/(?P<print_order_id>[0-9]+)/details', custom_admin_print_order_views.print_order_details, name="print_order_details"),

    url(r'^transactions/', custom_admin_transaction_views.transactions_list, name="transactions"),    

    url(r'^payment_requests/',custom_admin_payment_request_views.payment_requests, name="payment_requests")
]